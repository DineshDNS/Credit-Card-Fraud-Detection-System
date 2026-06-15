import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import Header from "../components/Header";
import PageContent from "../components/PageContent";

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
  LineChart,
  Line
} from "recharts";

import {
  FaCreditCard,
  FaExclamationTriangle,
  FaPercentage,
  FaShieldAlt,
  FaBell,
  FaEnvelope
} from "react-icons/fa";

function Dashboard() {

  const [stats, setStats] = useState({
    total_transactions: 0,
    fraud_count: 0,
    fraud_rate: 0,
  });

  const [riskData, setRiskData] =
    useState([]);

  const [trendData, setTrendData] =
    useState([]);

  const [advancedStats, setAdvancedStats] =
    useState({
      high_risk: 0,
      medium_risk: 0,
      email_alerts: 0,
    });

const [recentAlerts, setRecentAlerts] =
  useState([]);

  useEffect(() => {

    const fetchDashboardData =
      async () => {

        try {

          const statsResponse =
            await api.get(
              "/dashboard/stats"
            );

          setStats(
            statsResponse.data
          );

          const riskResponse =
            await api.get(
              "/dashboard/risk-distribution"
            );

          setRiskData([
            {
              risk: "Low",
              count:
                riskResponse.data.low,
            },
            {
              risk: "Medium",
              count:
                riskResponse.data.medium,
            },
            {
              risk: "High",
              count:
                riskResponse.data.high,
            },
          ]);

          const trendResponse =
            await api.get(
              "/dashboard/fraud-trends"
            );

          setTrendData(
            trendResponse.data
          );

          const advancedResponse =
            await api.get(
              "/dashboard/advanced-stats"
            );

          setAdvancedStats(
            advancedResponse.data
          );

          const alertsResponse =
            await api.get(
              "/dashboard/recent-alerts"
            );

          setRecentAlerts(
            alertsResponse.data
          );

        } catch (error) {

          console.error(
            "Dashboard Error:",
            error
          );

        }
      };

    fetchDashboardData();

    const interval =
      setInterval(
        fetchDashboardData,
        5000
      );

    return () =>
      clearInterval(
        interval
      );


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

    <div className="bg-gray-100 min-h-screen">

      <Sidebar />

      <Header title="Credit Card Fraud Detection Dashboard" />

      <PageContent>

        <div className="grid md:grid-cols-3 xl:grid-cols-3 gap-5">

          <StatCard
            title="Total Transactions"
            value={stats.total_transactions}
            icon={<FaCreditCard />}
            color="bg-blue-600"
          />

          <StatCard
            title="Fraud Count"
            value={stats.fraud_count}
            icon={<FaExclamationTriangle />}
            color="bg-red-600"
          />

          <StatCard
            title="Fraud Rate (%)"
            value={`${stats.fraud_rate}%`}
            icon={<FaPercentage />}
            color="bg-orange-500"
          />

          <StatCard
            title="High Risk Alerts"
            value={advancedStats.high_risk}
            icon={<FaShieldAlt />}
            color="bg-red-700"
          />

          <StatCard
            title="Medium Risk Alerts"
            value={advancedStats.medium_risk}
            icon={<FaBell />}
            color="bg-yellow-500"
          />

          <StatCard
            title="Email Alerts Sent"
            value={advancedStats.email_alerts}
            icon={<FaEnvelope />}
            color="bg-green-600"
          />

        </div>

        {/* Row 1 */}

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

        {/* Row 2 */}

        <div className="mt-8">

          <div className="bg-white p-6 rounded-lg shadow">

            <h2 className="text-2xl font-bold mb-4">
              Risk Level Distribution
            </h2>

            <ResponsiveContainer
              width="100%"
              height={350}
            >

              <BarChart
                data={riskData}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="risk"
                />

                <YAxis />

                <Tooltip />

                <Legend />

                <Bar
                  dataKey="count"
                  fill="#f97316"
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        {/* Row 3 */}

        <div className="mt-8">

          <div className="bg-white p-6 rounded-lg shadow">

            <h2 className="text-2xl font-bold mb-4">
              Daily Fraud Trend
            </h2>

            <ResponsiveContainer
              width="100%"
              height={350}
            >

              <LineChart
                data={trendData}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="date"
                />

                <YAxis />

                <Tooltip />

                <Legend />

                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#ef4444"
                  strokeWidth={3}
                />

              </LineChart>

            </ResponsiveContainer>

            

          </div>

        </div>

        <div className="mt-8">

          <div className="bg-white p-6 rounded-lg shadow">

            <h2 className="text-2xl font-bold mb-4">
              Recent Fraud Alerts
            </h2>

            {recentAlerts.length > 0 ? (

              <div className="space-y-4">

                {recentAlerts.map(
                  (alert, index) => (

                    <div
                      key={index}
                      className="
                        border
                        rounded-lg
                        p-4
                        flex
                        justify-between
                        items-center
                      "
                    >

                      <div>

                        <div className="font-semibold">
                          {alert.transaction_id}
                        </div>

                        <div className="text-gray-500 text-sm">
                          {new Date(
                            alert.predicted_at
                          ).toLocaleString()}
                        </div>

                      </div>

                      <span
                        className="
                          bg-red-100
                          text-red-700
                          px-3
                          py-1
                          rounded-full
                          font-semibold
                        "
                      >
                        {alert.risk_level}
                      </span>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="text-gray-500">
                No fraud alerts available
              </div>

            )}

          </div>

        </div>
        </PageContent>

        </div>
  );
}

export default Dashboard;