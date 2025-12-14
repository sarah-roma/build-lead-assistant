import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CreateCollection from '../create_collection';

describe('CreateCollection', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test('renders and creates a collection', async () => {
    // Mock fetch response for POST
    global.fetch.mockResolvedValueOnce({
      json: async () => ({ message: 'Collection created' })
    });

    render(<CreateCollection />);

    const input = screen.getByPlaceholderText('Collection Name');
    const button = screen.getByText('Create');

    fireEvent.change(input, { target: { value: 'test-collection' } });
    fireEvent.click(button);

    await waitFor(() => expect(screen.getByText(/Collection created/)).toBeInTheDocument());
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});
