import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";

function Alerts() {

  const [alerts, setAlerts] =
    useState([]);

  useEffect(() => {

    fetchAlerts();

  }, []);

  const fetchAlerts = async () => {

    try {

      const response =
        await api.get("/alerts");

      setAlerts(
        response.data || []
      );

    } catch (error) {

      console.error(
        "Error fetching alerts:",
        error
      );

      setAlerts([]);

    }

  };

  const updateStatus = async (
    alertId,
    status
  ) => {

    try {

      await api.put(
        `/alerts/${alertId}?status=${status}`
      );

      setAlerts((prevAlerts) =>
        prevAlerts.map((alert) =>
          alert.alert_id === alertId
            ? {
                ...alert,
                alert_status: status,
              }
            : alert
        )
      );

    } catch (error) {

      console.error(
        "Error updating alert:",
        error
      );

    }

  };

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-100 min-h-screen">

        <h1 className="text-4xl font-bold mb-6">
          Alerts
        </h1>

        <div className="bg-white rounded-lg shadow overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="bg-gray-200">

                <th className="p-3 text-left">
                  Alert ID
                </th>

                <th className="p-3 text-left">
                  Transaction ID
                </th>

                <th className="p-3 text-left">
                  Alert Type
                </th>

                <th className="p-3 text-left">
                  Status
                </th>

                <th className="p-3 text-left">
                  Created At
                </th>

              </tr>

            </thead>

            <tbody>

              {alerts.length > 0 ? (

                alerts.map((alert) => (

                  <tr
                    key={alert.alert_id}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="p-3">
                      {alert.alert_id}
                    </td>

                    <td className="p-3">
                      {alert.transaction_id}
                    </td>

                    <td className="p-3">
                      {alert.alert_type}
                    </td>

                    <td className="p-3">

                      <div className="flex flex-wrap gap-2">

                        <button
                          onClick={() =>
                            updateStatus(
                              alert.alert_id,
                              "Pending"
                            )
                          }
                          className="px-2 py-1 bg-yellow-500 text-white rounded text-sm"
                        >
                          Pending
                        </button>

                        <button
                          onClick={() =>
                            updateStatus(
                              alert.alert_id,
                              "Investigating"
                            )
                          }
                          className="px-2 py-1 bg-blue-500 text-white rounded text-sm"
                        >
                          Investigating
                        </button>

                        <button
                          onClick={() =>
                            updateStatus(
                              alert.alert_id,
                              "Resolved"
                            )
                          }
                          className="px-2 py-1 bg-green-500 text-white rounded text-sm"
                        >
                          Resolved
                        </button>

                      </div>

                      <div className="mt-2">

                        <span
                          className={`px-3 py-1 rounded-full font-semibold text-sm ${
                            alert.alert_status === "Resolved"
                              ? "bg-green-100 text-green-700"
                              : alert.alert_status === "Investigating"
                              ? "bg-blue-100 text-blue-700"
                              : "bg-yellow-100 text-yellow-700"
                          }`}
                        >
                          {alert.alert_status}
                        </span>

                      </div>

                    </td>

                    <td className="p-3">
                      {new Date(
                        alert.created_at
                      ).toLocaleString()}
                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan="5"
                    className="text-center p-6"
                  >
                    No alerts found
                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Alerts;