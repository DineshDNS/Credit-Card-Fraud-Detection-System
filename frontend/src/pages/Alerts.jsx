import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";

import {
  FaSearch,
  FaCheckCircle,
  FaTimes
} from "react-icons/fa";

function Alerts() {

  const [alerts, setAlerts] =
    useState([]);

  const [selectedAlert, setSelectedAlert] =
    useState(null);

  const [toast, setToast] =
    useState("");

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

      setAlerts(
        (prevAlerts) =>

          prevAlerts.map(
            (alert) =>

              alert.alert_id === alertId

                ? {
                    ...alert,
                    alert_status: status
                  }

                : alert
          )
      );

      setSelectedAlert(null);

      setToast(
        `Alert marked as ${status}`
      );

      setTimeout(() => {

        setToast("");

      }, 3000);

    } catch (error) {

      console.error(
        "Error updating alert:",
        error
      );

    }

  };

  return (

    <div className="bg-gray-100 min-h-screen">

      <Sidebar />

      <div className="ml-64 p-8">

        <h1 className="text-4xl font-bold mb-8">

          Fraud Alerts Center

        </h1>

        {

          toast && (

            <div
              className="
                mb-6
                bg-green-100
                border
                border-green-300
                text-green-700
                p-4
                rounded-lg
                shadow
              "
            >

              {toast}

            </div>

          )

        }

        <div
          className="
            bg-white
            rounded-xl
            shadow-lg
            overflow-auto
          "
        >

          <table
            className="
              min-w-full
            "
          >

            <thead>

              <tr
                className="
                  bg-gray-200
                "
              >

                <th className="p-4 text-left">
                  Transaction
                </th>

                <th className="p-4 text-left">
                  Risk Level
                </th>

                <th className="p-4 text-left">
                  Message
                </th>

                <th className="p-4 text-left">
                  Status
                </th>

                <th className="p-4 text-left">
                  Created Time
                </th>

                <th className="p-4 text-left">
                  Actions
                </th>

              </tr>

            </thead>

            <tbody>

              {

                alerts.length > 0

                ? alerts.map(
                    (alert) => (

                      <tr
                        key={
                          alert.alert_id
                        }
                        className="
                          border-b
                          hover:bg-gray-50
                        "
                      >

                        <td className="p-4 font-medium">

                          {
                            alert.transaction_id
                          }

                        </td>

                        <td className="p-4">

                          <span
                            className={`
                              px-3
                              py-1
                              rounded-full
                              font-semibold
                              ${
                                alert.risk_level === "High"
                                  ? "bg-red-100 text-red-700"
                                  : alert.risk_level === "Medium"
                                  ? "bg-orange-100 text-orange-700"
                                  : "bg-green-100 text-green-700"
                              }
                            `}
                          >

                            {
                              alert.risk_level
                            }

                          </span>

                        </td>

                        <td className="p-4">

                          {
                            alert.message
                          }

                        </td>

                        <td className="p-4">

                          <span
                            className={`
                              px-3
                              py-1
                              rounded-full
                              font-semibold
                              ${
                                alert.alert_status === "Resolved"
                                  ? "bg-green-100 text-green-700"
                                  : alert.alert_status === "Investigating"
                                  ? "bg-blue-100 text-blue-700"
                                  : "bg-yellow-100 text-yellow-700"
                              }
                            `}
                          >

                            {
                              alert.alert_status
                            }

                          </span>

                        </td>

                        <td className="p-4">

                          {new Date(
                            alert.created_at
                          ).toLocaleString()}

                        </td>

                        <td className="p-4">

                          <button
                            onClick={() =>
                              setSelectedAlert(
                                alert
                              )
                            }
                            className="
                              flex
                              items-center
                              gap-2
                              bg-blue-600
                              text-white
                              px-3
                              py-2
                              rounded
                              hover:bg-blue-700
                            "
                          >

                            <FaSearch />

                            Investigate

                          </button>

                        </td>

                      </tr>

                    )
                  )

                : (

                  <tr>

                    <td
                      colSpan="6"
                      className="
                        text-center
                        p-10
                      "
                    >

                      No Alerts Found

                    </td>

                  </tr>

                )

              }

            </tbody>

          </table>

        </div>

        {

          selectedAlert && (

            <div
              className="
                fixed
                inset-0
                bg-black/50
                flex
                justify-center
                items-center
                z-50
              "
            >

              <div
                className="
                  bg-white
                  p-8
                  rounded-xl
                  shadow-xl
                  w-[600px]
                "
              >

                <div
                  className="
                    flex
                    justify-between
                    items-center
                    mb-6
                  "
                >

                  <h2
                    className="
                      text-2xl
                      font-bold
                    "
                  >

                    Fraud Investigation

                  </h2>

                  <button
                    onClick={() =>
                      setSelectedAlert(
                        null
                      )
                    }
                  >

                    <FaTimes />

                  </button>

                </div>

                <div
                  className="
                    space-y-4
                  "
                >

                  <p>

                    <strong>
                      Transaction ID:
                    </strong>

                    {" "}

                    {
                      selectedAlert.transaction_id
                    }

                  </p>

                  <p>

                    <strong>
                      Risk Level:
                    </strong>

                    {" "}

                    {
                      selectedAlert.risk_level
                    }

                  </p>

                  <p>

                    <strong>
                      Message:
                    </strong>

                    {" "}

                    {
                      selectedAlert.message
                    }

                  </p>

                  <p>

                    <strong>
                      Status:
                    </strong>

                    {" "}

                    {
                      selectedAlert.alert_status
                    }

                  </p>

                </div>

                <div
                  className="
                    flex
                    gap-4
                    mt-8
                  "
                >

                  <button
                    onClick={() =>
                      updateStatus(
                        selectedAlert.alert_id,
                        "Investigating"
                      )
                    }
                    className="
                      bg-blue-600
                      text-white
                      px-4
                      py-2
                      rounded
                      hover:bg-blue-700
                    "
                  >

                    Investigating

                  </button>

                  <button
                    onClick={() =>
                      updateStatus(
                        selectedAlert.alert_id,
                        "Resolved"
                      )
                    }
                    className="
                      flex
                      items-center
                      gap-2
                      bg-green-600
                      text-white
                      px-4
                      py-2
                      rounded
                      hover:bg-green-700
                    "
                  >

                    <FaCheckCircle />

                    Resolve

                  </button>

                </div>

              </div>

            </div>

          )

        }

      </div>

    </div>

  );

}

export default Alerts;