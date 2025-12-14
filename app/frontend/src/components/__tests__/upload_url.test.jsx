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
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ ok: true }) });

    render(<UploadURL />);

    await waitFor(() => expect(screen.getByDisplayValue('colA')).toBeInTheDocument());

    const input = screen.getByPlaceholderText('URL');
    fireEvent.change(input, { target: { value: 'http://example.com' } });
    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText(/"ok": true/)).toBeInTheDocument());
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
