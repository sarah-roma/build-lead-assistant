import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import * as utils from '../utils';

describe('App integration', () => {
  beforeEach(() => {
    jest.restoreAllMocks();
    global.fetch = jest.fn();
  });

  test('navigates between tabs and uploads text', async () => {
    // When UploadText mounts it will call fetchCollections; return a default
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['col-integration']);

    // Mock upload text fetch response
    global.fetch.mockResolvedValueOnce({ json: async () => ({ status: 'ok' }) });

    render(<App />);

    // By default, Create Collection panel heading should be visible
    expect(screen.getByRole('heading', { name: /Create Collection/i })).toBeInTheDocument();

    // Navigate to Upload Text
    fireEvent.click(screen.getByText('Upload Text'));

    // Wait for the select to be populated with collections
    await waitFor(() => expect(screen.getByDisplayValue('col-integration')).toBeInTheDocument());

    // Fill textarea and upload
    fireEvent.change(screen.getByPlaceholderText('Information'), { target: { value: 'integration info' } });
    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText(/"status": "ok"/)).toBeInTheDocument());
  });

  test('uploads files via UI flow', async () => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['files-integration']);
    global.fetch.mockResolvedValueOnce({ json: async () => ({ uploaded: true }) });

    render(<App />);

    // Navigate to Upload Files
    fireEvent.click(screen.getByText('Upload Files'));

    await waitFor(() => expect(screen.getByDisplayValue('files-integration')).toBeInTheDocument());

    const file = new File(['content'], 'file.txt', { type: 'text/plain' });
    const fileInput = document.querySelector('input[type="file"]');
    fireEvent.change(fileInput, { target: { files: [file] } });

    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText(/"uploaded": true/)).toBeInTheDocument());
  });
});
