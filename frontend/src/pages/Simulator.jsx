import { useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";

function Simulator() {

  const [transactionId, setTransactionId] =
    useState("");

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const handlePredict = async () => {

    if (!transactionId) {

      alert(
        "Enter Transaction ID"
      );

      return;
    }

    try {

      setLoading(true);

      const response =
        await api.post(
          `/predict/${transactionId}`
        );

      setResult(
        response.data
      );

    } catch (error) {

      console.error(error);

      alert(
        "Prediction Failed"
      );

    } finally {

      setLoading(false);

    }

  };

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-100 min-h-screen">

        <h1 className="text-4xl font-bold mb-8">
          Prediction Simulator
        </h1>

        <div className="bg-white p-6 rounded-lg shadow max-w-2xl">

          <label className="block mb-2 font-semibold">
            Transaction ID
          </label>

          <input
            type="text"
            value={transactionId}
            onChange={(e) =>
              setTransactionId(
                e.target.value
              )
            }
            placeholder="TXN0081610"
            className="
              w-full
              border
              rounded
              px-4
              py-2
              mb-4
            "
          />

          <button
            onClick={handlePredict}
            disabled={loading}
            className="
              bg-blue-600
              text-white
              px-6
              py-2
              rounded
            "
          >
            {loading
              ? "Predicting..."
              : "Predict"}
          </button>

        </div>

        {result && (

          <div className="bg-white p-6 rounded-lg shadow mt-6 max-w-2xl">

            <h2 className="text-2xl font-bold mb-4">
              Prediction Result
            </h2>

            <p>
              <strong>
                Transaction ID:
              </strong>{" "}
              {result.transaction_id}
            </p>

            <p>
              <strong>
                Fraud Probability:
              </strong>{" "}
              {(
                result.fraud_probability * 100
              ).toFixed(2)}
              %
            </p>

            <p>
              <strong>
                Prediction:
              </strong>{" "}
              {result.prediction}
            </p>

            <p>
              <strong>
                Risk Level:
              </strong>{" "}
              {result.risk_level}
            </p>

          </div>

        )}

      </div>

    </div>
  );
}

export default Simulator;