import {
  FaUserShield
} from "react-icons/fa";

function Header({ title }) {

  return (

    <div
      className="
        fixed
        top-0
        left-64
        right-0
        z-40
        bg-gray-100
      "
    >

      <header
        className="
          h-24
          bg-gradient-to-r
          from-blue-900
          via-blue-800
          to-indigo-900
          shadow-lg

          flex
          items-center
          justify-between

          px-8

          text-white
        "
      >

        <div>

          <h1
            className="
              text-3xl
              font-bold
            "
          >
            {title}
          </h1>

          <p
            className="
              text-blue-200
              text-sm
              mt-1
            "
          >
            Credit Card Fraud Detection System
          </p>

        </div>

        <div
          className="
            flex
            items-center
            gap-4

            bg-white/10
            backdrop-blur-sm

            px-5
            py-3

            rounded-xl
          "
        >

          <div
            className="
              w-12
              h-12

              rounded-full

              bg-white

              flex
              items-center
              justify-center
            "
          >

            <FaUserShield
              className="
                text-blue-900
                text-xl
              "
            />

          </div>

          <div>

            <p
              className="
                font-semibold
              "
            >
              Administrator
            </p>

            <p
              className="
                text-xs
                text-blue-200
              "
            >
              Fraud Monitoring Team
            </p>

          </div>

        </div>

      </header>

    </div>

  );

}

export default Header;