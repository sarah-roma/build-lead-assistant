import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UploadFiles from '../upload_files';
import * as utils from '../../utils';

describe('UploadFiles', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['filesCol']);
    global.fetch = jest.fn();
  });

  afterEach(() => jest.restoreAllMocks());

  test('allows selecting files and uploading', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ uploaded: true }) });

    render(<UploadFiles />);

    await waitFor(() => expect(screen.getByDisplayValue('filesCol')).toBeInTheDocument());

    const file = new File(['hello'], 'hello.txt', { type: 'text/plain' });
    // Find the native file input and simulate selecting files
    const fileInput = document.querySelector('input[type="file"]');
    fireEvent.change(fileInput, { target: { files: [file] } });

    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText(/"uploaded": true/)).toBeInTheDocument());
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
