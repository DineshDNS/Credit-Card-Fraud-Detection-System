import { useEffect, useState } from "react";
import api from "../api/api";
import Sidebar from "../components/Sidebar";

function Transactions() {

  const [transactions, setTransactions] =
    useState([]);

  const [filter, setFilter] =
    useState("all");

  const [search, setSearch] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [totalPages, setTotalPages] =
    useState(1);

  const [totalRecords, setTotalRecords] =
    useState(0);

  const PAGE_SIZE = 50;

  useEffect(() => {

    const fetchTransactions = async () => {

      try {

        const response =
          await api.get(
            `/transactions?transaction_type=${filter}&search=${search}&page=${page}&page_size=${PAGE_SIZE}`
          );

        setTransactions(
          response.data.transactions || []
        );

        setTotalPages(
          response.data.total_pages || 1
        );

        setTotalRecords(
          response.data.total_records || 0
        );

      } catch (error) {

        console.error(
          "Error fetching transactions:",
          error
        );

        setTransactions([]);

      }

    };

    fetchTransactions();

  }, [filter, page, search]);

  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-100 min-h-screen">

        <h1 className="text-4xl font-bold mb-6">
          Transactions
        </h1>

        {/* Summary */}

        <div className="mb-4 font-semibold">
          Total Records: {totalRecords}
        </div>

        {/* Search + Filter */}

        <div className="flex flex-wrap gap-4 mb-6">

          <input
            type="text"
            placeholder="Search Transaction ID..."
            value={search}
            onChange={(e) => {

              setSearch(
                e.target.value
              );

              setPage(1);

            }}
            className="
              border
              rounded
              px-3
              py-2
              bg-white
              w-80
            "
          />

          <select
            value={filter}
            onChange={(e) => {

              setFilter(
                e.target.value
              );

              setPage(1);

            }}
            className="
              border
              rounded
              px-3
              py-2
              bg-white
            "
          >

            <option value="all">
              All Transactions
            </option>

            <option value="genuine">
              Genuine Transactions
            </option>

            <option value="fraud">
              Fraud Transactions
            </option>

          </select>

        </div>

        {/* Transactions Table */}

        <div className="bg-white rounded-lg shadow overflow-x-auto">

          <table className="w-full">

            <thead>

              <tr className="bg-gray-200">

                <th className="p-3 text-left">
                  Transaction ID
                </th>

                <th className="p-3 text-left">
                  User ID
                </th>

                <th className="p-3 text-left">
                  Merchant
                </th>

                <th className="p-3 text-left">
                  Location
                </th>

                <th className="p-3 text-left">
                  Amount
                </th>

                <th className="p-3 text-left">
                  Status
                </th>

              </tr>

            </thead>

            <tbody>

              {transactions.length > 0 ? (

                transactions.map((txn) => (

                  <tr
                    key={txn.transaction_id}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="p-3">
                      {txn.transaction_id}
                    </td>

                    <td className="p-3">
                      {txn.user_id}
                    </td>

                    <td className="p-3">
                      {txn.merchant}
                    </td>

                    <td className="p-3">
                      {txn.location}
                    </td>

                    <td className="p-3">
                      ₹{Number(
                        txn.amount
                      ).toLocaleString()}
                    </td>

                    <td className="p-3">

                      {txn.actual_class === 1 ? (

                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-semibold">
                          Fraud
                        </span>

                      ) : (

                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full font-semibold">
                          Genuine
                        </span>

                      )}

                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan="6"
                    className="text-center p-6"
                  >
                    No transactions found
                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

        {/* Pagination */}

        <div className="flex justify-center items-center gap-4 mt-6">

          <button
            disabled={page === 1}
            onClick={() =>
              setPage(page - 1)
            }
            className="
              px-4
              py-2
              bg-blue-600
              text-white
              rounded
              disabled:bg-gray-400
            "
          >
            Previous
          </button>

          <span className="font-semibold">
            Page {page} of {totalPages}
          </span>

          <button
            disabled={
              page === totalPages
            }
            onClick={() =>
              setPage(page + 1)
            }
            className="
              px-4
              py-2
              bg-blue-600
              text-white
              rounded
              disabled:bg-gray-400
            "
          >
            Next
          </button>

        </div>

      </div>

    </div>
  );
}

export default Transactions;