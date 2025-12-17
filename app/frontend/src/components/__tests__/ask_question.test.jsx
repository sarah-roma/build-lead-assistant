import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AskQuestion from '../ask_question';
import * as utils from '../../utils';

describe('AskQuestion', () => {
  beforeEach(() => {
    jest.spyOn(utils, 'fetchCollections').mockResolvedValue(['qaCol']);
    global.fetch = jest.fn();
  });

  afterEach(() => jest.restoreAllMocks());

  test('submits question and displays response', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ answer: 'Yes' }) });

    render(<AskQuestion />);

    await waitFor(() => expect(screen.getByDisplayValue('qaCol')).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText('Your Question'), { target: { value: 'Is it working?' } });
    fireEvent.click(screen.getByText('Submit'));

    await waitFor(() => expect(screen.getByText(/"answer": "Yes"/)).toBeInTheDocument());
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
