import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';

function ImpactSummary() {
  const [data, setData] = useState([]);
  useEffect(() => {
    axios.get('/architecture-packages/123/impact-summary').then(res => {
      setData([
        { name: 'KPI Count', value: res.data.kpi_count },
        { name: 'Aligned', value: res.data.aligned },
        { name: 'Coverage', value: res.data.coverage },
        { name: 'Goal Alignment', value: res.data.goal_alignment_score }
      ]);
    });
  }, []);
  return (
    <div>
      <h2>KPI Impact Summary</h2>
      <BarChart width={400} height={200} data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="value" fill="#8884d8" />
      </BarChart>
    </div>
  );
}

export default ImpactSummary;
