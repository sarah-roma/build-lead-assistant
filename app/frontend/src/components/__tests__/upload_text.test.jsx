import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UploadText from '../upload_text';
import * as utils from '../../utils';

describe('UploadText', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['col1']);
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders and uploads text', async () => {
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'success', title: 'Upload successful', message: 'Uploaded' }) });

    render(<UploadText />);

    // Wait for collections to load and select to be populated
    await waitFor(() => expect(screen.getByDisplayValue('col1')).toBeInTheDocument());

    const textarea = screen.getByPlaceholderText('Information');
    const button = screen.getByText('Upload');

    fireEvent.change(textarea, { target: { value: 'some information' } });
    fireEvent.click(button);

    // Expect the notification title/message to appear
    await waitFor(() => expect(screen.getByText('Upload successful')).toBeInTheDocument());
    expect(screen.getByText('Uploaded')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
