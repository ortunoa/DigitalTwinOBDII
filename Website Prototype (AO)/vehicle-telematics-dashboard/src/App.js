import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query';
import { ResponsiveLine } from '@nivo/line';
import 'tailwindcss/tailwind.css';

const queryClient = new QueryClient();

const fetchData = async (time) => {
  const response = await axios.post('http://localhost:8086/api/v2/query', `
    from(bucket: "digitaltwin")
      |> range(start: -10s)
      |> filter(fn: (r) => r["_measurement"] == "telemetry")
      |> filter(fn: (r) => r["_field"] == "AirFlowRate" or r["_field"] == "ThrottlePosition" or r["_field"] == "EngineLoad")
      |> aggregateWindow(every: 1s, fn: mean)
      |> yield(name: "mean")
  `, {
    headers: {
      'Authorization': 'Token -6ZrnMmAsURPlBWhCNhicxSipDy5HZoLKo8s49aku8cAm3fqRb_G8rELFwYoEpvyZPGrq9Z6bV8tIvRahqrxFw==',
      'Content-Type': 'application/vnd.flux',
    },
    params: {
      org: 'localinflux',
    },
  });

  // const data = response.data.trim().split('\n').slice(1);

  const data = response.data.trim().split('\n').slice(1).map((line) => {
    const [time, value] = line.split(',');
    return { x: new Date(time), y: parseFloat(value) };
  });
  console.log(data);
  return data;
};

function TelematicsPlot() {
  const [currentTime, setCurrentTime] = useState(Date.now());
  const { data, refetch } = useQuery(['telemetry', currentTime], () => fetchData(currentTime), {
    enabled: false,
    retry: false,
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(Date.now());
      refetch();
    }, 1000);
    return () => clearInterval(interval);
  }, [refetch]);

  return (
    <div className="h-full w-full">
      <ResponsiveLine
        data={[{ id: 'telemetry', data }]}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'time', format: 'native' }}
        yScale={{ type: 'linear', min: 'auto', max: 'auto', stacked: false, reverse: false }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          format: '%H:%M:%S',
          tickValues: 'every second',
          orient: 'bottom',
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'Time',
          legendOffset: 36,
          legendPosition: 'middle',
        }}
        axisLeft={{
          orient: 'left',
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: 'Value',
          legendOffset: -40,
          legendPosition: 'middle',
        }}
        colors={{ scheme: 'nivo' }}
        pointSize={10}
        pointColor={{ theme: 'background' }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabelYOffset={-12}
        useMesh={true}
      />
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="w-full max-w-6xl p-4 bg-white shadow-md rounded-md">
          <h1 className="text-2xl font-bold mb-4 text-gray-700">
            Vehicle Telematics Dashboard
          </h1>
          <div className="w-full h-96">
            <TelematicsPlot />
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
