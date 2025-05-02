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

export { applyType };
