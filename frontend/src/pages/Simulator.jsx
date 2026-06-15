import {
  useEffect,
  useState
} from "react";

import api from "../api/api";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import PageContent from "../components/PageContent";

import {
  FaPlay,
  FaStop,
  FaBolt,
  FaCheckCircle,
  FaTimesCircle,
  FaCreditCard
} from "react-icons/fa";

function Simulator() {

  const [running, setRunning] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [transactions, setTransactions] =
    useState([]);

  const fetchStatus = async () => {

    try {

      const response =
        await api.get(
          "/simulator/status"
        );

      setRunning(
        Boolean(
          response.data.running
        )
      );

    } catch (error) {

      console.error(error);

      setRunning(false);

    }

  };

  const fetchTransactions =
    async () => {

      try {

        const response =
          await api.get(
            "/simulator/recent-transactions"
          );

        setTransactions(
          response.data || []
        );

      } catch (error) {

        console.error(error);

      }

    };

  useEffect(() => {

    fetchStatus();

    fetchTransactions();

    const interval =
      setInterval(() => {

        fetchStatus();

        fetchTransactions();

      }, 2000);

    return () =>
      clearInterval(interval);

  }, []);

  const startSimulation =
    async () => {

      try {

        setLoading(true);

        await api.post(
          "/simulator/start"
        );

        setRunning(true);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }

    };

  const stopSimulation =
    async () => {

      try {

        setLoading(true);

        await api.post(
          "/simulator/stop"
        );

        setRunning(false);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);

      }

    };

  return (

    <div className="bg-gray-100 min-h-screen">

      <Sidebar />

      <Header
        title="Live Transaction Simulator"
      />

      <PageContent>

        <div className="bg-white rounded-xl shadow-lg p-8">

          <div className="flex items-center gap-4 mb-8">

            <FaBolt
              className="
                text-yellow-500
                text-4xl
              "
            />

            <div>

              <h2
                className="
                  text-3xl
                  font-bold
                "
              >
                Live Fraud Simulator
              </h2>

              <p className="text-gray-500">
                Real-time fraud monitoring
                and transaction generation
              </p>

            </div>

          </div>

          <div
            className="
              bg-gray-50
              border
              rounded-xl
              p-6
              mb-8
            "
          >

            <div
              className="
                flex
                justify-between
                items-center
              "
            >

              <div>

                <h3 className="text-xl font-semibold">
                  Simulator Status
                </h3>

                <p className="text-gray-500">
                  Background fraud engine
                </p>

              </div>

              {running ? (

                <span
                  className="
                    bg-green-100
                    text-green-700
                    px-4
                    py-2
                    rounded-full
                    flex
                    items-center
                    gap-2
                    font-semibold
                  "
                >
                  <FaCheckCircle />
                  Running
                </span>

              ) : (

                <span
                  className="
                    bg-red-100
                    text-red-700
                    px-4
                    py-2
                    rounded-full
                    flex
                    items-center
                    gap-2
                    font-semibold
                  "
                >
                  <FaTimesCircle />
                  Stopped
                </span>

              )}

            </div>

          </div>

          <div className="flex gap-4 mb-8">

            <button

              disabled={
                running || loading
              }

              onClick={
                startSimulation
              }

              className="
                bg-green-600
                hover:bg-green-700
                text-white
                px-6
                py-3
                rounded-lg
                flex
                items-center
                gap-3
                disabled:opacity-50
              "
            >

              <FaPlay />

              Start Simulator

            </button>

            <button

              disabled={
                !running || loading
              }

              onClick={
                stopSimulation
              }

              className="
                bg-red-600
                hover:bg-red-700
                text-white
                px-6
                py-3
                rounded-lg
                flex
                items-center
                gap-3
                disabled:opacity-50
              "
            >

              <FaStop />

              Stop Simulator

            </button>

          </div>

          <div
            className="
              grid
              md:grid-cols-3
              gap-6
              mb-10
            "
          >

            <div className="bg-blue-50 p-5 rounded-xl">
              <h3 className="font-bold">
                Multiple Users
              </h3>
              <p>
                Generates transactions
                for 10 demo customers.
              </p>
            </div>

            <div className="bg-yellow-50 p-5 rounded-xl">
              <h3 className="font-bold">
                Fraud Rate
              </h3>
              <p>
                Approximately
                10% fraud traffic.
              </p>
            </div>

            <div className="bg-green-50 p-5 rounded-xl">
              <h3 className="font-bold">
                Email Alerts
              </h3>
              <p>
                Fraud alerts sent
                automatically.
              </p>
            </div>

          </div>

          <div
            className="
              bg-white
              border
              rounded-xl
              overflow-hidden
            "
          >

            <div
              className="
                p-4
                border-b
                flex
                items-center
                gap-3
              "
            >

              <FaCreditCard />

              <h3 className="text-xl font-bold">
                Live Transaction Feed
              </h3>

            </div>

            <table className="w-full">

              <thead className="bg-gray-100">

                <tr>

                  <th className="p-3 text-left">
                    Transaction ID
                  </th>

                  <th className="p-3 text-left">
                    User
                  </th>

                  <th className="p-3 text-left">
                    Merchant
                  </th>

                  <th className="p-3 text-left">
                    Amount
                  </th>

                  <th className="p-3 text-left">
                    Time
                  </th>

                </tr>

              </thead>

              <tbody>

                {transactions.map(
                  (txn) => (

                    <tr
                      key={
                        txn.transaction_id
                      }
                      className="border-t"
                    >

                      <td className="p-3">
                        {
                          txn.transaction_id
                        }
                      </td>

                      <td className="p-3">
                        {
                          txn.user_id
                        }
                      </td>

                      <td className="p-3">
                        {
                          txn.merchant
                        }
                      </td>

                      <td className="p-3">
                        ₹
                        {Number(
                          txn.amount
                        ).toLocaleString()}
                      </td>

                      <td className="p-3">
                        {
                          new Date(
                            txn.transaction_time
                          ).toLocaleString()
                        }
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        </div>

      </PageContent>

    </div>

  );

}

export default Simulator;