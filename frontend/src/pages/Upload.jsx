import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import PageContent from "../components/PageContent";

import {
  FaUpload,
  FaFileExcel,
  FaDatabase
} from "react-icons/fa";

function Upload() {

  const [file, setFile] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [uploading, setUploading] =
    useState(false);

  const fetchHistory = async () => {

    try {

      const response =
        await api.get(
          "/upload-history"
        );

      setHistory(
        response.data
      );

    } catch (error) {

      console.error(
        "History Error:",
        error
      );

    }

  };

  useEffect(() => {

    fetchHistory();

  }, []);

  const handleUpload =
    async () => {

      if (!file) {

        alert(
          "Please select a file"
        );

        return;
      }

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {

        setUploading(true);

        const response =
          await api.post(
            "/upload-transactions",
            formData,
            {
              headers: {
                "Content-Type":
                  "multipart/form-data"
              }
            }
          );

        setResult(
          response.data
        );

        setFile(null);

        document.getElementById(
          "upload-file"
        ).value = "";

        fetchHistory();

      } catch (error) {

        console.error(error);

        alert(
          "Upload Failed"
        );

      } finally {

        setUploading(false);

      }

    };

  return (

    <div className="bg-gray-100 min-h-screen">

      <Sidebar />
      <Header title="Upload Transactions" />

      <PageContent>


        {/* Upload Card */}

        <div
          className="
            bg-white
            rounded-xl
            shadow-lg
            p-8
            border
            mb-8
          "
        >

          <div
            className="
              flex
              items-center
              gap-3
              mb-6
            "
          >

            <FaFileExcel
              className="
                text-green-600
                text-4xl
              "
            />

            <h2 className="text-3xl font-bold">

              Upload CSV / XLSX

            </h2>

          </div>

          <p className="text-gray-500 mb-6">

            Upload transaction files for
            fraud detection analysis.

          </p>

          <input
            id="upload-file"
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) =>
              setFile(
                e.target.files[0]
              )
            }
            className="
              border
              rounded-lg
              p-4
              w-full
              mb-4
            "
          />

          {

            file && (

              <div
                className="
                  mb-4
                  text-blue-600
                  font-medium
                "
              >

                Selected File:
                {" "}
                {file.name}

              </div>

            )

          }

          <button
            onClick={handleUpload}
            disabled={uploading}
            className="
              flex
              items-center
              gap-2
              bg-blue-600
              text-white
              px-6
              py-3
              rounded-lg
              hover:bg-blue-700
              disabled:bg-gray-400
              disabled:cursor-not-allowed
            "
          >

            {

              uploading ? (

                <>

                  <div
                    className="
                      animate-spin
                      rounded-full
                      h-5
                      w-5
                      border-b-2
                      border-white
                    "
                  />

                  Uploading...

                </>

              ) : (

                <>

                  <FaUpload />

                  Upload Transactions

                </>

              )

            }

          </button>

        </div>

        {/* Success Message */}

        {

          result && (

            <div
              className="
                bg-green-100
                border
                border-green-300
                text-green-700
                p-4
                rounded-lg
                mb-6
              "
            >

              ✅ File uploaded successfully:

              {" "}

              {result.uploaded_file}

            </div>

          )

        }

        {/* Upload Summary */}

        {

          result && (

            <div className="mb-10">

              <h2
                className="
                  text-2xl
                  font-bold
                  mb-4
                "
              >

                Upload Summary

              </h2>

              <div
                className="
                  grid
                  md:grid-cols-4
                  gap-6
                "
              >

                <div
                  className="
                    bg-white
                    p-6
                    rounded-lg
                    shadow
                  "
                >

                  <h3 className="font-semibold">

                    Customers

                  </h3>

                  <p
                    className="
                      text-3xl
                      font-bold
                      mt-2
                    "
                  >

                    {
                      result.customers_inserted
                    }

                  </p>

                </div>

                <div
                  className="
                    bg-white
                    p-6
                    rounded-lg
                    shadow
                  "
                >

                  <h3 className="font-semibold">

                    Transactions

                  </h3>

                  <p
                    className="
                      text-3xl
                      font-bold
                      mt-2
                    "
                  >

                    {
                      result.transactions_inserted
                    }

                  </p>

                </div>

                <div
                  className="
                    bg-white
                    p-6
                    rounded-lg
                    shadow
                  "
                >

                  <h3 className="font-semibold">

                    Predictions

                  </h3>

                  <p
                    className="
                      text-3xl
                      font-bold
                      mt-2
                    "
                  >

                    {
                      result.predictions_created
                    }

                  </p>

                </div>

                <div
                  className="
                    bg-white
                    p-6
                    rounded-lg
                    shadow
                  "
                >

                  <h3
                    className="
                      font-semibold
                      text-red-600
                    "
                  >

                    Frauds Detected

                  </h3>

                  <p
                    className="
                      text-3xl
                      font-bold
                      text-red-600
                      mt-2
                    "
                  >

                    {
                      result.fraud_detected
                    }

                  </p>

                </div>

              </div>

            </div>

          )

        }

        {/* Upload History */}

        <div>

          <div
            className="
              flex
              items-center
              gap-3
              mb-4
            "
          >

            <FaDatabase
              className="
                text-blue-600
                text-2xl
              "
            />

            <h2
              className="
                text-2xl
                font-bold
              "
            >

              Upload History

            </h2>

          </div>

          <div
            className="
              bg-white
              rounded-lg
              shadow
              overflow-auto
            "
          >

            <table className="min-w-full">

              <thead>

                <tr
                  className="
                    bg-gray-200
                  "
                >

                  <th className="p-4 text-left">
                    File Name
                  </th>

                  <th className="p-4 text-left">
                    Records
                  </th>

                  <th className="p-4 text-left">
                    Frauds
                  </th>

                  <th className="p-4 text-left">
                    Uploaded At
                  </th>

                </tr>

              </thead>

              <tbody>

                {

                  history.length > 0 ? (

                    history.map(
                      (item) => (

                        <tr
                          key={
                            item.upload_id
                          }
                          className="
                            border-b
                            hover:bg-gray-50
                          "
                        >

                          <td className="p-4">

                            {
                              item.file_name
                            }

                          </td>

                          <td className="p-4">

                            {
                              item.records_count
                            }

                          </td>

                          <td className="p-4">

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

                              {
                                item.fraud_detected
                              }

                            </span>

                          </td>

                          <td className="p-4">

                            {new Date(
                              item.uploaded_at
                            ).toLocaleString()}

                          </td>

                        </tr>

                      )
                    )

                  ) : (

                    <tr>

                      <td
                        colSpan="4"
                        className="
                          text-center
                          p-6
                        "
                      >

                        No Upload History Found

                      </td>

                    </tr>

                  )

                }

              </tbody>

            </table>

          </div>

        </div>

      </PageContent>

    </div>

  );

}

export default Upload;