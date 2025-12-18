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
    // Component expects res.ok and returns { answer }
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ answer: 'Yes' }) });

    render(<AskQuestion />);

    await waitFor(() => expect(screen.getByDisplayValue('qaCol')).toBeInTheDocument());

    // The TextInput label is 'Your question' (lowercase q) and has id 'question-input'
    fireEvent.change(screen.getByPlaceholderText('Type your question here'), { target: { value: 'Is it working?' } });
    // Button text is 'Ask'
    fireEvent.click(screen.getByText('Ask'));

    // Component displays the answer in a paragraph under the heading 'Answer:'
    await waitFor(() => expect(screen.getByText('Answer:')).toBeInTheDocument());
    expect(screen.getByText('Yes')).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
