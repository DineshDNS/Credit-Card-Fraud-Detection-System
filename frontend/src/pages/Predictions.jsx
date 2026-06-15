import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import PageContent from "../components/PageContent";

import {
  FaBrain,
  FaExclamationTriangle,
  FaShieldAlt,
  FaChartLine,
  FaSearch,
  FaTimes,
  FaCheckCircle
} from "react-icons/fa";

function Predictions() {

  const [predictions, setPredictions] =
    useState([]);

  const [search, setSearch] =
    useState("");

  const [selectedPrediction, setSelectedPrediction] =
    useState(null);

  useEffect(() => {

    fetchPredictions();

  }, []);

  const fetchPredictions = async () => {

    try {

      const response =
        await api.get(
          "/fraud-predictions"
        );

      setPredictions(
        response.data || []
      );

    } catch (error) {

      console.error(
        "Error fetching predictions:",
        error
      );

      setPredictions([]);

    }

  };

  const filteredPredictions =

    predictions.filter(
      (prediction) =>

        prediction.transaction_id
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )
    );

  const fraudCount =

    predictions.filter(
      (prediction) =>
        prediction.prediction ===
        "Fraud"
    ).length;

  const genuineCount =

    predictions.filter(
      (prediction) =>
        prediction.prediction ===
        "Legitimate"
    ).length;

  const highRiskCount =

    predictions.filter(
      (prediction) =>
        prediction.risk_level ===
        "High"
    ).length;

  return (

    <div className="bg-gray-100 min-h-screen">

      <Sidebar />
      <Header title="Prediction Intelligence Center" />

      <PageContent>

        {/* Summary Cards */}

        <div
          className="
            grid
            md:grid-cols-4
            gap-6
            mb-8
          "
        >

          <div className="bg-white p-6 rounded-xl shadow">

            <div className="flex items-center gap-3">

              <FaBrain className="text-indigo-600 text-3xl" />

              <div>

                <p className="text-gray-500">
                  Total Predictions
                </p>

                <h2 className="text-3xl font-bold">
                  {predictions.length}
                </h2>

              </div>

            </div>

          </div>

          <div className="bg-white p-6 rounded-xl shadow">

            <div className="flex items-center gap-3">

              <FaExclamationTriangle className="text-red-600 text-3xl" />

              <div>

                <p className="text-gray-500">
                  Fraud Detected
                </p>

                <h2 className="text-3xl font-bold text-red-600">
                  {fraudCount}
                </h2>

              </div>

            </div>

          </div>

          <div className="bg-white p-6 rounded-xl shadow">

            <div className="flex items-center gap-3">

              <FaShieldAlt className="text-green-600 text-3xl" />

              <div>

                <p className="text-gray-500">
                  Genuine
                </p>

                <h2 className="text-3xl font-bold text-green-600">
                  {genuineCount}
                </h2>

              </div>

            </div>

          </div>

          <div className="bg-white p-6 rounded-xl shadow">

            <div className="flex items-center gap-3">

              <FaChartLine className="text-orange-600 text-3xl" />

              <div>

                <p className="text-gray-500">
                  High Risk
                </p>

                <h2 className="text-3xl font-bold text-orange-600">
                  {highRiskCount}
                </h2>

              </div>

            </div>

          </div>

        </div>

        {/* Search */}

        <div className="bg-white p-5 rounded-xl shadow mb-6">

          <div className="flex items-center gap-3">

            <FaSearch className="text-gray-500" />

            <input
              type="text"
              placeholder="Search Transaction ID..."
              value={search}
              onChange={(e) =>
                setSearch(
                  e.target.value
                )
              }
              className="
                w-full
                border
                rounded-lg
                p-3
                outline-none
              "
            />

          </div>

        </div>

        {/* Table */}

        <div
          className="
            bg-white
            rounded-xl
            shadow-lg
            overflow-auto
          "
        >

          <table className="min-w-full">

            <thead>

              <tr className="bg-gray-200">

                <th className="p-4 text-left">
                  Prediction ID
                </th>

                <th className="p-4 text-left">
                  Transaction ID
                </th>

                <th className="p-4 text-left">
                  Prediction
                </th>

                <th className="p-4 text-left">
                  Risk Level
                </th>

                <th className="p-4 text-left">
                  Fraud Probability
                </th>

                <th className="p-4 text-left">
                  Predicted At
                </th>

              </tr>

            </thead>

            <tbody>

              {

                filteredPredictions.length > 0

                ? filteredPredictions.map(
                    (prediction) => (

                      <tr
                        key={
                          prediction.prediction_id
                        } onClick={() => setSelectedPrediction(prediction)}
                        className="
                          border-b
                          hover:bg-blue-50
                          cursor-pointer
                        "
                      >

                        <td className="p-4">

                          {
                            prediction.prediction_id
                          }

                        </td>

                        <td className="p-4 font-medium">

                          {
                            prediction.transaction_id
                          }

                        </td>

                        <td className="p-4">

                          {

                            prediction.prediction ===
                            "Fraud"

                            ? (

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

                                Fraud

                              </span>

                            )

                            : (

                              <span
                                className="
                                  bg-green-100
                                  text-green-700
                                  px-3
                                  py-1
                                  rounded-full
                                  font-semibold
                                "
                              >

                                Genuine

                              </span>

                            )

                          }

                        </td>

                        <td className="p-4">

                          {

                            prediction.risk_level ===
                            "High"

                            ? (

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

                                High

                              </span>

                            )

                            : prediction.risk_level ===
                              "Medium"

                            ? (

                              <span
                                className="
                                  bg-orange-100
                                  text-orange-700
                                  px-3
                                  py-1
                                  rounded-full
                                  font-semibold
                                "
                              >

                                Medium

                              </span>

                            )

                            : (

                              <span
                                className="
                                  bg-green-100
                                  text-green-700
                                  px-3
                                  py-1
                                  rounded-full
                                  font-semibold
                                "
                              >

                                Low

                              </span>

                            )

                          }

                        </td>

                        <td className="p-4">

                          <span
                            className="
                              bg-blue-100
                              text-blue-700
                              px-3
                              py-1
                              rounded-full
                              font-semibold
                            "
                          >

                            {
                              (
                                prediction.fraud_probability
                                * 100
                              ).toFixed(2)
                            }%

                          </span>

                        </td>

                        <td className="p-4">

                          {new Date(
                            prediction.predicted_at
                          ).toLocaleString()}

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

                      No Predictions Found

                    </td>

                  </tr>

                )

              }

            </tbody>

          </table>

        </div>

        {
          selectedPrediction && (

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
                  w-[650px]
                  p-8
                  rounded-xl
                  shadow-xl
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
                    Prediction Details
                  </h2>

                  <button
                    onClick={() =>
                      setSelectedPrediction(
                        null
                      )
                    }
                  >
                    <FaTimes />
                  </button>

                </div>

                <div className="space-y-4">

                  <p>
                    <strong>
                      Transaction ID:
                    </strong>
                    {" "}
                    {
                      selectedPrediction.transaction_id
                    }
                  </p>

                  <p>
                    <strong>
                      Prediction:
                    </strong>
                    {" "}
                    {
                      selectedPrediction.prediction
                    }
                  </p>

                  <p>
                    <strong>
                      Risk Level:
                    </strong>
                    {" "}
                    {
                      selectedPrediction.risk_level
                    }
                  </p>

                  <p>
                    <strong>
                      Fraud Probability:
                    </strong>
                    {" "}
                    {
                      (
                        selectedPrediction
                          .fraud_probability
                        * 100
                      ).toFixed(2)
                    }%
                  </p>

                  <p>
                    <strong>
                      Predicted At:
                    </strong>
                    {" "}
                    {
                      new Date(
                        selectedPrediction
                          .predicted_at
                      ).toLocaleString()
                    }
                  </p>

                </div>


                   <div
                    className="
                      mt-8
                      bg-red-50
                      border
                      border-red-200
                      p-5
                      rounded-lg
                    "
                  >

                    <h3
                      className="
                        text-lg
                        font-bold
                        text-red-700
                        mb-4
                      "
                    >
                      Explainable AI Analysis
                    </h3>

                    {

                      selectedPrediction.explanation

                      ? (

                        JSON.parse(
                          selectedPrediction.explanation
                        ).map(
                          (
                            reason,
                            index
                          ) => (

                            <div
                              key={index}
                              className="
                                flex
                                items-center
                                gap-3
                                mb-3
                              "
                            >

                              <FaCheckCircle
                                className="
                                  text-red-600
                                "
                              />

                              <span
                                className="
                                  font-medium
                                  text-gray-700
                                "
                              >
                                {reason}
                              </span>

                            </div>

                          )
                        )

                      )

                      : (

                        <div
                          className="
                            text-gray-500
                          "
                        >
                          No explanation available
                        </div>

                      )

                    }

                </div>

              </div>

            </div>

          )
        }

      </PageContent>

    </div>

  );

}

export default Predictions;