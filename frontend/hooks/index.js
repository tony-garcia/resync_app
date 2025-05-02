import { useState, useEffect, useRef } from 'react';

import axios from 'axios';

/**
 * Hook for fetching data asynchronously from an API
 * @param {object} config - axios request config (https://github.com/axios/axios)
 * @param {*} [initialState] - default initial state of the data (defaults to empty array)
 * @param {function} [cb] - optional callback which receives the returned data as the argument
 * @returns
 */
function useAPI(initialConfig, initialState, cb = () => null) {
  const [requestConfig, setRequestConfig] = useState(initialConfig);
  const [data, setData] = useState(initialState || []);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(Boolean(initialConfig));
  const [error, setError] = useState(null);

  // stabilize the callback to use it in useEffect hook below
  const callback = useRef(cb);

  /**
   * Used to refresh the data using the same request configuration
   */
  const refresh = () => setIsLoaded(false);

  /**
   * Used to fetch data with the same hook but different request config
   * @param {object} config -- The axios request config for the API call
   */
  const fetchData = (config) => {
    setIsLoaded(false);
    setRequestConfig(config);
  };

  const clearData = () => {
    setData(initialState);
  };

  useEffect(() => {
    /**
     * Uses axios to send a request to an API using the config passed to the hook.
     */
    let isCurrent = true;
    const doFetch = async () => {
      if (requestConfig && isCurrent) {
        setIsLoading(true);
        try {
          const response = await axios(requestConfig);
          if (isCurrent && response?.data) {
            setData(response.data);
            callback.current(response.data);
            return response;
          }
        } catch (e) {
          // don't worry if redirect is about to happen for auth
          setError(e);
        } finally {
          if (isCurrent) {
            setIsLoading(false);
            setIsLoaded(true);
          }
        }
      }
    };
    if (!isLoaded && Boolean(requestConfig)) {
      doFetch();
    }
    return () => {
      isCurrent = false;
    };
  }, [requestConfig, isLoaded]);

  return { data, isLoading, isLoaded, error, setData, clearData, refresh, fetchData };
}

/**
 * Hook for referencing the value from a previous render
 * @param {*} value -- the value to create a previous reference to
 * @returns {*} the previous value
 */
function usePrevious(value) {
  const ref = useRef();

  // store current value in the ref (only initially and when the value changes)
  useEffect(() => {
    ref.current = value;
  }, [value]);

  // return previous value (the useEffect hook above happens asyncronously)
  return ref.current;
}

export { useAPI, usePrevious };
