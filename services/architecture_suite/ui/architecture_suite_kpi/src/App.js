import React from 'react';
import ImpactSummary from './components/ImpactSummary';
import TraceDrilldown from './components/TraceDrilldown';

function App() {
  return (
    <div>
      <h1>Architecture Suite KPI Dashboard</h1>
      <ImpactSummary />
      <TraceDrilldown />
    </div>
  );
}

export default App;
