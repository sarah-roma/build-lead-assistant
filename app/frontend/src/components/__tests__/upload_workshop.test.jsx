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
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'created' }) });

    render(<UploadWorkshop />);

    await waitFor(() => expect(screen.getByDisplayValue('wsCol')).toBeInTheDocument());

    // Fill in fields according to the current form structure
    fireEvent.change(screen.getByPlaceholderText('e.g. 12 March 2024'), { target: { value: '12 March 2024' } });
    fireEvent.change(screen.getByPlaceholderText('https://app.mural.co/...'), { target: { value: 'https://app.mural.co/example' } });

    // Attendee inputs don't have id attributes; get all textboxes and target the attendee name
    const textboxes = screen.getAllByRole('textbox');
    // Index mapping: 0 = workshop-date, 1 = mural-url, 2 = attendee name
    fireEvent.change(textboxes[2], { target: { value: 'Alice' } });

    fireEvent.click(screen.getByText('Upload Workshop'));

    // Component shows success notification title when successful
    await waitFor(() => expect(screen.getByText('Workshop ingested successfully')).toBeInTheDocument());
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
