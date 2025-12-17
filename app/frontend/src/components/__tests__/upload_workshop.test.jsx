import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UploadWorkshop from '../upload_workshop';
import * as utils from '../../utils';

describe('UploadWorkshop', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['wsCol']);
    global.fetch = jest.fn();
  });

  afterEach(() => jest.restoreAllMocks());

  test('sends workshop info via POST and shows response', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ status: 'created' }) });

    render(<UploadWorkshop />);

    await waitFor(() => expect(screen.getByDisplayValue('wsCol')).toBeInTheDocument());

    // Fill in fields according to the current form structure
    fireEvent.change(screen.getByPlaceholderText('e.g. 12 March 2024'), { target: { value: '12 March 2024' } });
    fireEvent.change(screen.getByPlaceholderText('https://app.mural.co/...'), { target: { value: 'https://app.mural.co/example' } });
    // Add attendee info so the form will include attendee fields (query by label)
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Alice' } });

    fireEvent.click(screen.getByText('Upload Workshop'));

    await waitFor(() => expect(screen.getByText(/"status": "created"/)).toBeInTheDocument());
    // Ensure the POST request was made
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
