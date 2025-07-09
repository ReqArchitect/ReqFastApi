// Monitoring Dashboard Frontend Panel
// Lightweight React component for live service status monitoring

class MonitoringDashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            services: {},
            summary: {},
            loading: true,
            error: null,
            criticalOnly: false,
            lastUpdate: null,
            autoRefresh: true
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
            }, 15000); // 15 seconds
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
            
            const params = new URLSearchParams();
            if (this.state.criticalOnly) {
                params.append('critical_only', 'true');
            }
            
            const response = await fetch(`/platform/status?${params}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            this.setState({
                services: data.services || {},
                summary: data.summary || {},
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
        // Log panel load for audit trail
        fetch('/api/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event: 'panel_load',
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                services_count: Object.keys(data.services || {}).length,
                critical_only: this.state.criticalOnly,
                summary: data.summary
            })
        }).catch(err => console.warn('Failed to log panel load:', err));
    }

    toggleCriticalOnly = () => {
        this.setState(prevState => ({
            criticalOnly: !prevState.criticalOnly
        }), () => {
            this.loadPlatformStatus();
        });
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

    getStatusColor(status) {
        switch (status) {
            case 'healthy': return 'bg-green-500';
            case 'degraded': return 'bg-yellow-500';
            case 'unhealthy': return 'bg-red-500';
            case 'timeout': return 'bg-orange-500';
            case 'unknown': return 'bg-gray-500';
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
            default: return '❓';
        }
    }

    renderServiceCard(serviceName, serviceData) {
        const status = serviceData.status || 'unknown';
        const responseTime = serviceData.response_time_ms || 0;
        const isCritical = serviceData.critical || false;
        const uptime = serviceData.uptime || 'N/A';
        const error = serviceData.error || null;
        const lastCheck = serviceData.last_check || 'Unknown';

        return (
            <div key={serviceName} className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                        <span className={`inline-block w-3 h-3 rounded-full ${this.getStatusColor(status)}`}></span>
                        <h3 className="text-lg font-semibold text-gray-800">
                            {serviceName}
                            {isCritical && <span className="ml-2 px-2 py-1 text-xs bg-red-100 text-red-800 rounded">CRITICAL</span>}
                        </h3>
                    </div>
                    <span className="text-2xl">{this.getStatusIcon(status)}</span>
                </div>
                
                <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex justify-between">
                        <span>Status:</span>
                        <span className={`font-medium ${status === 'healthy' ? 'text-green-600' : status === 'degraded' ? 'text-yellow-600' : 'text-red-600'}`}>
                            {status.toUpperCase()}
                        </span>
                    </div>
                    
                    <div className="flex justify-between">
                        <span>Response Time:</span>
                        <span className={responseTime > 1000 ? 'text-red-600 font-medium' : 'text-gray-600'}>
                            {responseTime}ms
                        </span>
                    </div>
                    
                    {uptime !== 'N/A' && (
                        <div className="flex justify-between">
                            <span>Uptime:</span>
                            <span className="text-gray-600">{uptime}</span>
                        </div>
                    )}
                    
                    <div className="flex justify-between">
                        <span>Last Check:</span>
                        <span className="text-gray-500 text-xs">
                            {new Date(lastCheck).toLocaleTimeString()}
                        </span>
                    </div>
                    
                    {error && (
                        <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
                            <span className="text-red-700 text-xs">
                                <strong>Error:</strong> {error}
                            </span>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    renderSummary() {
        const { summary } = this.state;
        if (!summary.total_services) return null;

        return (
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4">Platform Summary</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{summary.total_services}</div>
                        <div className="text-sm text-gray-600">Total Services</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{summary.healthy_services}</div>
                        <div className="text-sm text-gray-600">Healthy</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{summary.unhealthy_services}</div>
                        <div className="text-sm text-gray-600">Unhealthy</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">{summary.success_rate}%</div>
                        <div className="text-sm text-gray-600">Success Rate</div>
                    </div>
                </div>
                
                {summary.critical_services > 0 && (
                    <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
                        <div className="flex items-center justify-between">
                            <span className="text-yellow-800 font-medium">
                                Critical Services: {summary.healthy_critical_services}/{summary.critical_services} Healthy
                            </span>
                            <span className={`text-sm px-2 py-1 rounded ${
                                summary.critical_success_rate === 100 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                                {summary.critical_success_rate}%
                            </span>
                        </div>
                    </div>
                )}
            </div>
        );
    }

    render() {
        const { services, loading, error, criticalOnly, autoRefresh, lastUpdate } = this.state;
        
        const filteredServices = criticalOnly 
            ? Object.fromEntries(Object.entries(services).filter(([_, data]) => data.critical))
            : services;

        return (
            <div className="min-h-screen bg-gray-50 p-6">
                <div className="max-w-7xl mx-auto">
                    {/* Header */}
                    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <h1 className="text-3xl font-bold text-gray-800">ReqArchitect Platform Monitor</h1>
                                <p className="text-gray-600 mt-1">Real-time service health monitoring</p>
                            </div>
                            <div className="flex items-center space-x-4">
                                <div className="flex items-center space-x-2">
                                    <label className="flex items-center">
                                        <input
                                            type="checkbox"
                                            checked={criticalOnly}
                                            onChange={this.toggleCriticalOnly}
                                            className="mr-2"
                                        />
                                        <span className="text-sm text-gray-700">Critical Only</span>
                                    </label>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <label className="flex items-center">
                                        <input
                                            type="checkbox"
                                            checked={autoRefresh}
                                            onChange={this.toggleAutoRefresh}
                                            className="mr-2"
                                        />
                                        <span className="text-sm text-gray-700">Auto Refresh</span>
                                    </label>
                                </div>
                                <button
                                    onClick={() => this.loadPlatformStatus()}
                                    disabled={loading}
                                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                                >
                                    {loading ? 'Loading...' : 'Refresh'}
                                </button>
                            </div>
                        </div>
                        
                        {lastUpdate && (
                            <div className="mt-4 text-sm text-gray-500">
                                Last updated: {lastUpdate}
                            </div>
                        )}
                    </div>

                    {/* Error Display */}
                    {error && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                            <div className="flex items-center">
                                <span className="text-red-500 mr-2">❌</span>
                                <span className="text-red-700">Error loading platform status: {error}</span>
                            </div>
                        </div>
                    )}

                    {/* Summary */}
                    {this.renderSummary()}

                    {/* Services Grid */}
                    {loading ? (
                        <div className="text-center py-12">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                            <p className="mt-4 text-gray-600">Loading platform status...</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {Object.entries(filteredServices).map(([serviceName, serviceData]) =>
                                this.renderServiceCard(serviceName, serviceData)
                            )}
                        </div>
                    )}

                    {/* Empty State */}
                    {!loading && Object.keys(filteredServices).length === 0 && (
                        <div className="text-center py-12">
                            <div className="text-gray-400 text-6xl mb-4">📊</div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No services found</h3>
                            <p className="text-gray-600">
                                {criticalOnly 
                                    ? "No critical services are currently running."
                                    : "No services are currently available."
                                }
                            </p>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('monitoring-dashboard');
    if (container) {
        ReactDOM.render(<MonitoringDashboard />, container);
    }
}); 