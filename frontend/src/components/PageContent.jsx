function PageContent({ children }) {

  return (

    <div
      className="
        ml-64
        pt-32
        px-8
        pb-8
        min-h-[calc(100vh-96px)]
        bg-gray-100
      "
    >

      {children}

    </div>

  );

}

export default PageContent;