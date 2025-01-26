import React, { useState, useEffect } from "react";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("http://localhost:8000/summary/monthly/");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        setData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  // Destructure the data for easier access
  const { income, expense, net_income } = data || {};

  return (
    <div>
      <h1 className="text-4xl font-bold text-blue-500">Dashboard</h1>
      <p className="mt-4 text-lg text-gray-600">Summary data for {data?.period}</p>

      <div className="mt-6 space-y-4">
        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Income</div>
          <div className="text-lg text-green-500">{income?.total}</div>
        </div>

        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Cash Income</div>
          <div className="text-lg text-green-500">{income?.cash}</div>
        </div>

        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Credit Income</div>
          <div className="text-lg text-green-500">{income?.credit}</div>
        </div>

        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Expense</div>
          <div className="text-lg text-red-500">{expense?.total}</div>
        </div>

        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Cash Expense</div>
          <div className="text-lg text-red-500">{expense?.cash}</div>
        </div>

        <div className="flex justify-between">
          <div className="text-lg font-semibold text-gray-700">Credit Expense</div>
          <div className="text-lg text-red-500">{expense?.credit}</div>
        </div>

        <div className="flex justify-between mt-4">
          <div className="text-lg font-semibold text-gray-700">Net Income</div>
          <div className="text-xl font-bold text-purple-500">{net_income}</div>
        </div>
      </div>
    </div>
  );
}
