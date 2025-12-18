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
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ status: 'success', title: 'Mural uploaded', message: 'Mural added' }) });

    render(<UploadMuralBoard />);

    await waitFor(() => expect(screen.getByDisplayValue('muralCol')).toBeInTheDocument());

    // Component uses placeholder 'https://app.mural.co/...'
    fireEvent.change(screen.getByPlaceholderText('https://app.mural.co/...'), { target: { value: 'http://mural.example' } });
    fireEvent.click(screen.getByText('Upload'));

    await waitFor(() => expect(screen.getByText('Mural uploaded')).toBeInTheDocument());
    expect(screen.getByText('Mural added')).toBeInTheDocument();
  });
});
