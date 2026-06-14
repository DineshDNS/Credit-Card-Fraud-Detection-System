import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";

function Predictions() {

  const [predictions, setPredictions] =
    useState([]);

  useEffect(() => {

    const fetchPredictions = async () => {

      try {

        const response =
          await api.get("/fraud-predictions");

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

    fetchPredictions();

  }, []);

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-100 min-h-screen">

        <h1 className="text-4xl font-bold mb-6">
          Predictions
        </h1>

        <div className="bg-white rounded-lg shadow overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="bg-gray-200">

                <th className="p-3 text-left">
                  Prediction ID
                </th>

                <th className="p-3 text-left">
                  Transaction ID
                </th>

                <th className="p-3 text-left">
                  Prediction
                </th>

                <th className="p-3 text-left">
                  Risk Level
                </th>

                <th className="p-3 text-left">
                  Fraud Probability
                </th>

                <th className="p-3 text-left">
                  Predicted At
                </th>

              </tr>

            </thead>

            <tbody>

              {predictions.length > 0 ? (

                predictions.map((prediction) => (

                  <tr
                    key={prediction.prediction_id}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="p-3">
                      {prediction.prediction_id}
                    </td>

                    <td className="p-3">
                      {prediction.transaction_id}
                    </td>

                    <td className="p-3">

                      {prediction.prediction === "Fraud" ? (

                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-semibold">
                          Fraud
                        </span>

                      ) : (

                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full font-semibold">
                          Genuine
                        </span>

                      )}

                    </td>

                    <td className="p-3">

                      {prediction.risk_level === "High" ? (

                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-semibold">
                          High
                        </span>

                      ) : prediction.risk_level === "Medium" ? (

                        <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full font-semibold">
                          Medium
                        </span>

                      ) : (

                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full font-semibold">
                          Low
                        </span>

                      )}

                    </td>

                    <td className="p-3">
                      {(prediction.fraud_probability * 100).toFixed(2)}%
                    </td>

                    <td className="p-3">
                      {new Date(
                        prediction.predicted_at
                      ).toLocaleString()}
                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan="6"
                    className="text-center p-6"
                  >
                    No predictions found
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

export default Predictions;