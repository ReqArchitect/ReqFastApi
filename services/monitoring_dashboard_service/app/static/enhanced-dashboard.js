// Enhanced Monitoring Dashboard Frontend
// Comprehensive React component for real-time service status monitoring

class EnhancedMonitoringDashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            services: {},
            servicesByLayer: {},
            summary: {},
            layers: [],
            loading: true,
            error: null,
            filters: {
                layer: null,
                status: null,
                discoveryMethod: null
            },
            lastUpdate: null,
            autoRefresh: true,
            refreshInterval: 30000, // 30 seconds
            selectedService: null,
            showVirtualServices: true
        };
        this.refreshInterval = null;
    }

    componentDidMount() {
        this.loadPlatformStatus();
        this.startAutoRefresh();
    }

    componentWillUnmount() {
        this.stopAutoRefresh();
    }

    startAutoRefresh() {
        if (this.state.autoRefresh) {
            this.refreshInterval = setInterval(() => {
                this.loadPlatformStatus();
            }, this.state.refreshInterval);
        }
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    async loadPlatformStatus() {
        try {
            this.setState({ loading: true, error: null });
            
            const response = await fetch('/platform/status?include_metrics=true');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            this.setState({
                services: data.services || {},
                servicesByLayer: data.services_by_layer || {},
                summary: data.summary || {},
                layers: data.layers || [],
                loading: false,
                lastUpdate: new Date().toLocaleTimeString(),
                error: null
            });
            
            // Log panel load for audit trail
            this.logPanelLoad(data);
            
        } catch (error) {
            console.error('Error loading platform status:', error);
            this.setState({
                loading: false,
                error: error.message
            });
        }
    }

    logPanelLoad(data) {
        fetch('/api/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event: 'enhanced_panel_load',
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                services_count: Object.keys(data.services || {}).length,
                layers_count: data.layers ? data.layers.length : 0,
                summary: data.summary
            })
        }).catch(err => console.warn('Failed to log panel load:', err));
    }

    toggleAutoRefresh = () => {
        this.setState(prevState => ({
            autoRefresh: !prevState.autoRefresh
        }), () => {
            if (this.state.autoRefresh) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });
    }

    setFilter = (filterType, value) => {
        this.setState(prevState => ({
            filters: {
                ...prevState.filters,
                [filterType]: prevState.filters[filterType] === value ? null : value
            }
        }));
    }

    toggleVirtualServices = () => {
        this.setState(prevState => ({
            showVirtualServices: !prevState.showVirtualServices
        }));
    }

    selectService = (serviceName) => {
        this.setState({
            selectedService: this.state.selectedService === serviceName ? null : serviceName
        });
    }

    getStatusColor(status) {
        switch (status) {
            case 'healthy': return 'bg-green-500';
            case 'degraded': return 'bg-yellow-500';
            case 'unhealthy': return 'bg-red-500';
            case 'timeout': return 'bg-orange-500';
            case 'unknown': return 'bg-gray-500';
            case 'virtual': return 'bg-purple-500';
            default: return 'bg-gray-400';
        }
    }

    getStatusIcon(status) {
        switch (status) {
            case 'healthy': return '✅';
            case 'degraded': return '⚠️';
            case 'unhealthy': return '❌';
            case 'timeout': return '⏰';
            case 'unknown': return '❓';
            case 'virtual': return '🟣';
            default: return '❓';
        }
    }

    getLayerColor(layer) {
        switch (layer.toLowerCase()) {
            case 'business': return 'layer-business';
            case 'application': return 'layer-application';
            case 'technology': return 'layer-technology';
            case 'infrastructure': return 'layer-infrastructure';
            case 'security': return 'layer-security';
            case 'motivation': return 'layer-motivation';
            default: return 'layer-business';
        }
    }

    getLayerIcon(layer) {
        switch (layer.toLowerCase()) {
            case 'business': return '💼';
            case 'application': return '🖥️';
            case 'technology': return '🔧';
            case 'infrastructure': return '🏗️';
            case 'security': return '🔒';
            case 'motivation': return '🎯';
            default: return '📋';
        }
    }

    formatLatency(latency) {
        if (!latency || latency === 0) return '-';
        if (latency < 100) return `${latency}ms`;
        if (latency < 1000) return `${latency}ms`;
        return `${(latency / 1000).toFixed(1)}s`;
    }

    formatLastChecked(timestamp) {
        if (!timestamp) return 'N/A';
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins}m ago`;
            if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
            return date.toLocaleDateString();
        } catch (e) {
            return 'Invalid';
        }
    }

    renderServiceCard(serviceName, serviceData) {
        const status = serviceData.status || 'unknown';
        const isVirtual = serviceData.is_virtual || false;
        const discoveryMethod = serviceData.discovery_method || 'unknown';
        const layer = serviceData.layer || 'unknown';
        const baseUrl = serviceData.base_url || '';
        const port = serviceData.port || 0;
        const description = serviceData.description || '';
        const lastHeartbeat = serviceData.last_heartbeat || '';
        const errorDetails = serviceData.error_details || '';

        // Apply filters
        if (this.state.filters.layer && layer.toLowerCase() !== this.state.filters.layer.toLowerCase()) return null;
        if (this.state.filters.status && status.toLowerCase() !== this.state.filters.status.toLowerCase()) return null;
        if (this.state.filters.discoveryMethod && discoveryMethod.toLowerCase() !== this.state.filters.discoveryMethod.toLowerCase()) return null;
        if (!this.state.showVirtualServices && isVirtual) return null;

        const isSelected = this.state.selectedService === serviceName;

        return (
            <div 
                key={serviceName} 
                className={`bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-all cursor-pointer ${this.getLayerColor(layer)} ${isSelected ? 'ring-2 ring-blue-500' : ''}`}
                onClick={() => this.selectService(serviceName)}
            >
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                        <span className={`inline-block w-3 h-3 rounded-full ${this.getStatusColor(status)}`}></span>
                        <h3 className="text-lg font-semibold text-gray-800">
                            {serviceName}
                            {isVirtual && <span className="ml-2 px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">VIRTUAL</span>}
                        </h3>
                    </div>
                    <div className="flex items-center space-x-2">
                        <span className="text-2xl">{this.getStatusIcon(status)}</span>
                        <span className="text-lg">{this.getLayerIcon(layer)}</span>
                    </div>
                </div>
                
                <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex justify-between">
                        <span>Status:</span>
                        <span className={`font-medium ${status === 'healthy' ? 'text-green-600' : status === 'degraded' ? 'text-yellow-600' : 'text-red-600'}`}>
                            {status.toUpperCase()}
                        </span>
                    </div>
                    
                    <div className="flex justify-between">
                        <span>Port:</span>
                        <span className="text-gray-600">{port}</span>
                    </div>
                    
                    <div className="flex justify-between">
                        <span>Discovery:</span>
                        <span className="text-gray-600">{discoveryMethod}</span>
                    </div>
                    
                    <div className="flex justify-between">
                        <span>Layer:</span>
                        <span className="text-gray-600 capitalize">{layer}</span>
                    </div>
                    
                    <div className="flex justify-between">
                        <span>Last Checked:</span>
                        <span className="text-gray-500 text-xs">
                            {this.formatLastChecked(lastHeartbeat)}
                        </span>
                    </div>
                    
                    {description && (
                        <div className="mt-2 p-2 bg-gray-50 rounded">
                            <span className="text-gray-700 text-xs">{description}</span>
                        </div>
                    )}
                    
                    {errorDetails && (
                        <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
                            <span className="text-red-700 text-xs">
                                <strong>Error:</strong> {errorDetails}
                            </span>
                        </div>
                    )}
                </div>

                {/* Direct Access Links */}
                {baseUrl && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex flex-wrap gap-2">
                            <a 
                                href={`${baseUrl}/health`} 
                                target="_blank" 
                                className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                                onClick={(e) => e.stopPropagation()}
                            >
                                Health
                            </a>
                            <a 
                                href={`${baseUrl}/docs`} 
                                target="_blank" 
                                className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded hover:bg-green-200"
                                onClick={(e) => e.stopPropagation()}
                            >
                                Docs
                            </a>
                            <a 
                                href={`${baseUrl}/openapi.json`} 
                                target="_blank" 
                                className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded hover:bg-purple-200"
                                onClick={(e) => e.stopPropagation()}
                            >
                                OpenAPI
                            </a>
                            <a 
                                href={`${baseUrl}/metrics`} 
                                target="_blank" 
                                className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded hover:bg-orange-200"
                                onClick={(e) => e.stopPropagation()}
                            >
                                Metrics
                            </a>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    renderServiceGrid() {
        const { servicesByLayer, layers } = this.state;
        
        if (Object.keys(servicesByLayer).length === 0) {
            return (
                <div className="text-center py-8">
                    <div className="text-gray-500 text-lg">No services found</div>
                </div>
            );
        }

        return (
            <div className="space-y-6">
                {layers.map(layer => {
                    const layerServices = servicesByLayer[layer] || [];
                    if (layerServices.length === 0) return null;

                    return (
                        <div key={layer} className="space-y-4">
                            <div className="flex items-center space-x-2">
                                <span className="text-2xl">{this.getLayerIcon(layer)}</span>
                                <h2 className="text-xl font-bold text-gray-800 capitalize">{layer} Layer</h2>
                                <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-sm">
                                    {layerServices.length} services
                                </span>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                {layerServices.map(service => this.renderServiceCard(service.service_name, service))}
                            </div>
                        </div>
                    );
                })}
            </div>
        );
    }

    renderFilters() {
        const { filters, layers, showVirtualServices } = this.state;
        const statuses = ['healthy', 'unhealthy', 'degraded', 'timeout', 'unknown', 'virtual'];
        const discoveryMethods = ['container_running', 'catalog_fallback', 'label_based'];

        return (
            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Filters</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {/* Layer Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Layer</label>
                        <div className="flex flex-wrap gap-2">
                            <button
                                onClick={() => this.setFilter('layer', null)}
                                className={`px-3 py-1 text-xs rounded ${!filters.layer ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                            >
                                All
                            </button>
                            {layers.map(layer => (
                                <button
                                    key={layer}
                                    onClick={() => this.setFilter('layer', layer)}
                                    className={`px-3 py-1 text-xs rounded ${filters.layer === layer ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                                >
                                    {layer}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Status Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                        <div className="flex flex-wrap gap-2">
                            <button
                                onClick={() => this.setFilter('status', null)}
                                className={`px-3 py-1 text-xs rounded ${!filters.status ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                            >
                                All
                            </button>
                            {statuses.map(status => (
                                <button
                                    key={status}
                                    onClick={() => this.setFilter('status', status)}
                                    className={`px-3 py-1 text-xs rounded ${filters.status === status ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                                >
                                    {status}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Discovery Method Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Discovery</label>
                        <div className="flex flex-wrap gap-2">
                            <button
                                onClick={() => this.setFilter('discoveryMethod', null)}
                                className={`px-3 py-1 text-xs rounded ${!filters.discoveryMethod ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                            >
                                All
                            </button>
                            {discoveryMethods.map(method => (
                                <button
                                    key={method}
                                    onClick={() => this.setFilter('discoveryMethod', method)}
                                    className={`px-3 py-1 text-xs rounded ${filters.discoveryMethod === method ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                                >
                                    {method}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Virtual Services Toggle */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Options</label>
                        <button
                            onClick={this.toggleVirtualServices}
                            className={`px-3 py-1 text-xs rounded ${showVirtualServices ? 'filter-active' : 'bg-gray-100 hover:bg-gray-200'}`}
                        >
                            {showVirtualServices ? 'Hide' : 'Show'} Virtual
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    renderSummary() {
        const { summary } = this.state;
        
        if (!summary) return null;

        return (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Platform Summary</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{summary.total_services || 0}</div>
                        <div className="text-sm text-gray-600">Total Services</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{summary.healthy_services || 0}</div>
                        <div className="text-sm text-gray-600">Healthy</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{summary.unhealthy_services || 0}</div>
                        <div className="text-sm text-gray-600">Unhealthy</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">{summary.virtual_services || 0}</div>
                        <div className="text-sm text-gray-600">Virtual</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">{summary.critical_services || 0}</div>
                        <div className="text-sm text-gray-600">Critical</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-indigo-600">{summary.success_rate || 0}%</div>
                        <div className="text-sm text-gray-600">Success Rate</div>
                    </div>
                </div>
                {summary.last_update && (
                    <div className="mt-4 text-center text-sm text-gray-500">
                        Last updated: {new Date(summary.last_update).toLocaleString()}
                    </div>
                )}
            </div>
        );
    }

    render() {
        const { loading, error, autoRefresh, lastUpdate } = this.state;

        if (loading) {
            return (
                <div className="min-h-screen bg-gray-50 p-6">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center py-12">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                            <div className="text-lg text-gray-600">Loading enhanced monitoring dashboard...</div>
                        </div>
                    </div>
                </div>
            );
        }

        if (error) {
            return (
                <div className="min-h-screen bg-gray-50 p-6">
                    <div className="max-w-7xl mx-auto">
                        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                            <div class="text-red-500 text-6xl mb-4">⚠️</div>
                            <h2 class="text-xl font-bold text-red-800 mb-2">Dashboard Error</h2>
                            <p class="text-red-700 mb-4">{error}</p>
                            <button onClick={() => this.loadPlatformStatus()} class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                                Retry
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return (
            <div className="min-h-screen bg-gray-50">
                {/* Header */}
                <div className="bg-white shadow-sm border-b">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between items-center py-4">
                            <div className="flex items-center space-x-4">
                                <h1 className="text-2xl font-bold text-gray-900">ReqArchitect Enhanced Platform Monitor</h1>
                                <div className="flex items-center space-x-2">
                                    <span className={`w-2 h-2 rounded-full ${autoRefresh ? 'bg-green-500' : 'bg-gray-400'}`}></span>
                                    <span className="text-sm text-gray-600">
                                        {autoRefresh ? 'Auto-refresh' : 'Manual'}
                                    </span>
                                </div>
                            </div>
                            <div className="flex items-center space-x-4">
                                <button
                                    onClick={this.toggleAutoRefresh}
                                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center space-x-2"
                                >
                                    <span className={autoRefresh ? 'refresh-indicator' : ''}>🔄</span>
                                    <span>{autoRefresh ? 'Stop' : 'Start'} Auto-refresh</span>
                                </button>
                                <button
                                    onClick={() => this.loadPlatformStatus()}
                                    className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                                >
                                    Refresh Now
                                </button>
                                {lastUpdate && (
                                    <span className="text-sm text-gray-500">
                                        Last: {lastUpdate}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content */}
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    {this.renderSummary()}
                    {this.renderFilters()}
                    {this.renderServiceGrid()}
                </div>
            </div>
        );
    }
}

// Render the enhanced dashboard
ReactDOM.render(
    <EnhancedMonitoringDashboard />,
    document.getElementById('enhanced-monitoring-dashboard')
); 