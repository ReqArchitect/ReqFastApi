import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TreeViewExplorer from './components/TreeViewExplorer';
import DetailPanel from './components/DetailPanel';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/model/tree" element={<TreeViewExplorer />} />
        <Route path="/model/:element/:id" element={<DetailPanel />} />
      </Routes>
    </Router>
  );
}

export default App;
