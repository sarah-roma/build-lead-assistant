// Setup file executed after the testing environment is set up.
// Adds helpful matchers like `toBeInTheDocument` via jest-dom.
// Note: newer versions of @testing-library/jest-dom export matchers from
// the package root (no `extend-expect` path), so import the package directly.
import '@testing-library/jest-dom';
