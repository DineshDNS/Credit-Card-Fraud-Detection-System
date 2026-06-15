function StatCard({
  title,
  value,
  icon,
  color
}) {

  return (

    <div
      className="
        bg-white
        rounded-xl
        shadow-lg
        border
        border-gray-100
        p-3

        hover:shadow-xl
        hover:-translate-y-1

        transition-all
        duration-300
      "
    >

      <div
        className="
          flex
          justify-between
          items-start
        "
      >

        <div>

          <p
            className="
              text-gray-500
              font-medium
              text-sm
            "
          >
            {title}
          </p>

          <h2
            className="
              text-3xl
              font-bold
              mt-2
              text-gray-800
            "
          >
            {value}
          </h2>

        </div>

        <div
          className={`
            ${color}
            w-10
            h-10
            rounded
            flex
            items-center
            justify-center
            text-white
            text-xl
            shadow-md
          `}
        >
          {icon}
        </div>

      </div>

    </div>

  );

}

export default StatCard;