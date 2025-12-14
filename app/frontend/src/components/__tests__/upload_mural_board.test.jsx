import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UploadMuralBoard from '../upload_mural_board';
import * as utils from '../../utils';

describe('UploadMuralBoard', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['muralCol']);
    global.fetch = jest.fn();
  });

  afterEach(() => jest.restoreAllMocks());

  test('uploads mural board url', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ ok: true }) });

    render(<UploadMuralBoard />);

    await waitFor(() => expect(screen.getByDisplayValue('muralCol')).toBeInTheDocument());

    fireEvent.change(screen.getByPlaceholderText('Mural Board URL'), { target: { value: 'http://mural.example' } });
    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText(/"ok": true/)).toBeInTheDocument());
  });
});
