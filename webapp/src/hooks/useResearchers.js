import { useState } from "react";


const useResearchers = (url, options) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchResearchers = async (params) => {
    const url = new URL("http://localhost/researchers");
    url.search = new URLSearchParams(params).toString();

    setData(null)
    setIsLoading(true);
    try {
      const resp = await fetch(url);
      const data = await resp.json();

      setData(data);
    } catch (e) {
      setData([]);
      setError(e);
    }
    setIsLoading(false);

    return data;
  };

  return { data, error, isLoading, fetchResearchers };
};

export default useResearchers;
