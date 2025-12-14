module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  transform: {
    '^.+\\.jsx?$': ['babel-jest', { configFile: './babel.config.cjs' }]
  },
  // Map static assets (css, images) to mock modules so Jest doesn't try to
  // parse them as JS. This keeps tests focused on JS/JSX behavior.
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/src/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|svg|png|jpg|jpeg)$': '<rootDir>/src/__mocks__/fileMock.js'
  },
  moduleFileExtensions: ['js', 'jsx', 'json', 'node'],
  testMatch: ['**/__tests__/**/*.test.{js,jsx}', '**/?(*.)+(spec|test).{js,jsx}']
};

