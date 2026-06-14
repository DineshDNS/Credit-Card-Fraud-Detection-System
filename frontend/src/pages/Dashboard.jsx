import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

function Dashboard() {

  const [stats, setStats] = useState({
    total_transactions: 0,
    fraud_count: 0,
    fraud_rate: 0,
  });

  useEffect(() => {

    const fetchStats = async () => {

      try {

        const response =
          await api.get(
            "/dashboard/stats"
          );

        setStats(
          response.data
        );

      } catch (error) {

        console.error(
          "Error fetching dashboard stats:",
          error
        );

      }

    };

    fetchStats();

  }, []);

  const pieData = [
    {
      name: "Fraud",
      value: stats.fraud_count,
    },
    {
      name: "Genuine",
      value:
        stats.total_transactions -
        stats.fraud_count,
    },
  ];

  const barData = [
    {
      category: "Total",
      count:
        stats.total_transactions,
    },
    {
      category: "Fraud",
      count:
        stats.fraud_count,
    },
  ];

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-100 min-h-screen">

        <h1 className="text-4xl font-bold mb-8">
          Credit Card Fraud Detection Dashboard
        </h1>

        {/* Stats Cards */}

        <div className="grid md:grid-cols-3 gap-6">

          <StatCard
            title="Total Transactions"
            value={stats.total_transactions.toLocaleString()}
          />

          <StatCard
            title="Fraud Count"
            value={stats.fraud_count}
          />

          <StatCard
            title="Fraud Rate (%)"
            value={stats.fraud_rate}
          />

        </div>

        {/* Charts Section */}

        <div className="grid lg:grid-cols-2 gap-6 mt-10">

          {/* Pie Chart */}

          <div className="bg-white p-6 rounded-lg shadow">

            <h2 className="text-2xl font-bold mb-4">
              Fraud vs Genuine Transactions
            </h2>

            <ResponsiveContainer
              width="100%"
              height={350}
            >

              <PieChart>

                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={120}
                  label
                >

                  <Cell fill="#ef4444" />

                  <Cell fill="#22c55e" />

                </Pie>

                <Tooltip />

                <Legend />

              </PieChart>

            </ResponsiveContainer>

          </div>

          {/* Bar Chart */}

          <div className="bg-white p-6 rounded-lg shadow">

            <h2 className="text-2xl font-bold mb-4">
              Fraud Statistics
            </h2>

            <ResponsiveContainer
              width="100%"
              height={350}
            >

              <BarChart
                data={barData}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="category"
                />

                <YAxis />

                <Tooltip />

                <Legend />

                <Bar
                  dataKey="count"
                  fill="#3b82f6"
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;