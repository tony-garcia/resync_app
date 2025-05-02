/**
 * Determines whether a string represents an integer, float, or should remain a string
 * And then casts the string to the guessed type
 * @param {string} str - The string to analyze
 * @returns {string | float | integer} - Returns the value cast as an integer, float, or string
 */
function applyType(str) {
  // Trim whitespace
  const trimmed = str.trim();

  // Empty string check
  if (trimmed === '') {
    return trimmed;
  }

  // Check if it's a valid number (integers and floats)
  if (/^[+-]?\d*\.?\d+$/.test(trimmed)) {
    // Check if it's an integer (no decimal point or only zeros after decimal)
    if (/^[+-]?\d+$/.test(trimmed) || /^[+-]?\d+\.0+$/.test(trimmed)) {
      return parseInt(trimmed, 10);
    }
    // It has a decimal point with non-zero numbers after it
    return parseFloat(trimmed);
  }

  // Everything else is a string (including scientific notation)
  return trimmed;
}

const initRDKit = (() => {
  let rdkitLoadingPromise;

  return () => {
    /**
     * Utility function ensuring there's only one call made to load RDKit
     * It returns a promise with the resolved RDKit API as value on success,
     * and a rejected promise with the error on failure.
     *
     * The RDKit API is also attached to the global object on successful load.
     */
    if (!rdkitLoadingPromise) {
      rdkitLoadingPromise = new Promise((resolve, reject) => {
        window
          .initRDKitModule()
          .then((RDKit) => {
            window.RDKit = RDKit;
            resolve(RDKit);
          })
          .catch((e) => {
            reject();
          });
      });
    }

    return rdkitLoadingPromise;
  };
})();

export { applyType, initRDKit };
