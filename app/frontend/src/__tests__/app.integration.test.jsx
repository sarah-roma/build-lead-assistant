import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock all child panel components to keep this test focused on App's
// navigation and rendering logic. Mocks return simple identifiable text.
jest.mock('../components/create_collection', () => ({
  __esModule: true,
  default: () => <div>Mock CreateCollection</div>,
}));
jest.mock('../components/upload_text', () => ({
  __esModule: true,
  default: () => <div>Mock UploadText</div>,
}));
jest.mock('../components/upload_url', () => ({
  __esModule: true,
  default: () => <div>Mock UploadURL</div>,
}));
jest.mock('../components/upload_mural_board', () => ({
  __esModule: true,
  default: () => <div>Mock UploadMuralBoard</div>,
}));
jest.mock('../components/upload_workshop', () => ({
  __esModule: true,
  default: () => <div>Mock UploadWorkshop</div>,
}));
jest.mock('../components/upload_files', () => ({
  __esModule: true,
  default: () => <div>Mock UploadFiles</div>,
}));
jest.mock('../components/ask_question', () => ({
  __esModule: true,
  default: () => <div>Mock AskQuestion</div>,
}));

// Import App after the mocks so its imports are replaced by the mocks above.
import App from '../App';

describe('App integration (navigation + panel rendering)', () => {
  test('renders header and initial panel (Create Collection)', () => {
    render(<App />);

    // Header
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();

    // Initial active panel should be the Create Collection mock
    expect(screen.getByText('Mock CreateCollection')).toBeInTheDocument();
  });

  test('navigates to Upload Text panel when link is clicked', async () => {
    render(<App />);

    const uploadText = screen.getByText('Upload Text');
    await userEvent.click(uploadText);

    // After clicking, the UploadText mock should be visible
    expect(screen.getByText('Mock UploadText')).toBeInTheDocument();
    // And the initial Create Collection mock should no longer be present
    expect(screen.queryByText('Mock CreateCollection')).not.toBeInTheDocument();
  });

  test('all side nav labels are present and switch panels', async () => {
    render(<App />);

    // Check a representative subset of tabs exist
    expect(screen.getByText('Upload URL')).toBeInTheDocument();
    expect(screen.getByText('Upload Mural Board')).toBeInTheDocument();
    expect(screen.getByText('Ask a Question')).toBeInTheDocument();

    // Click Upload URL and expect that mock
    await userEvent.click(screen.getByText('Upload URL'));
    expect(screen.getByText('Mock UploadURL')).toBeInTheDocument();

    // Click Ask a Question and expect that mock
    await userEvent.click(screen.getByText('Ask a Question'));
    expect(screen.getByText('Mock AskQuestion')).toBeInTheDocument();
  });
});
