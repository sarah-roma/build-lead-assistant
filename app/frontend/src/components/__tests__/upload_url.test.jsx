import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UploadURL from '../upload_url';
import * as utils from '../../utils';

describe('UploadURL', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['colA']);
    global.fetch = jest.fn();
  });

  afterEach(() => jest.restoreAllMocks());

  test('renders and uploads a URL', async () => {
    // Component expects res.ok and data.status === 'success'
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'success', title: 'Uploaded', message: 'URL added' }) });

    render(<UploadURL />);

    await waitFor(() => expect(screen.getByDisplayValue('colA')).toBeInTheDocument());

    // The component uses placeholder 'https://example.com/article'
    const input = screen.getByPlaceholderText('https://example.com/article');
    fireEvent.change(input, { target: { value: 'http://example.com' } });
    fireEvent.click(screen.getByText('Upload'));

    // Expect the success notification to show the server title/message
    await waitFor(() => expect(screen.getByText('Uploaded')).toBeInTheDocument());
    expect(screen.getByText('URL added')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
