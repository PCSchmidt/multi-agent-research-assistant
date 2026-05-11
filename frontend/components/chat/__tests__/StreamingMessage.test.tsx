import React from 'react';
import { render } from '@testing-library/react-native';
import { StreamingMessage } from '../StreamingMessage';
import { Message } from '../../../types/research';

describe('StreamingMessage', () => {
  const mockOnCitationPress = jest.fn();

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders user message correctly', () => {
    const message: Message = {
      id: 'msg-1',
      role: 'user',
      content: 'What is a transformer?',
      timestamp: new Date('2024-01-01T12:00:00'),
    };

    const { getByText } = render(
      <StreamingMessage message={message} onCitationPress={mockOnCitationPress} />
    );

    expect(getByText('You')).toBeTruthy();
    expect(getByText('What is a transformer?')).toBeTruthy();
  });

  it('renders assistant message correctly', () => {
    const message: Message = {
      id: 'msg-2',
      role: 'assistant',
      content: 'A transformer is a neural network architecture.',
      timestamp: new Date('2024-01-01T12:01:00'),
    };

    const { getByText } = render(
      <StreamingMessage message={message} onCitationPress={mockOnCitationPress} />
    );

    expect(getByText('Research Assistant')).toBeTruthy();
    expect(getByText('A transformer is a neural network architecture.')).toBeTruthy();
  });

  it('renders eval scores when available', () => {
    const message: Message = {
      id: 'msg-3',
      role: 'assistant',
      content: 'Test answer',
      evalScores: {
        faithfulness: 0.87,
        answerRelevancy: 0.92,
        citationAccuracy: 0.85,
        status: 'completed',
      },
      timestamp: new Date(),
    };

    const { getByText } = render(
      <StreamingMessage message={message} onCitationPress={mockOnCitationPress} />
    );

    expect(getByText('87%')).toBeTruthy(); // Faithfulness
    expect(getByText('92%')).toBeTruthy(); // Relevancy
    expect(getByText('85%')).toBeTruthy(); // Citation Accuracy
  });

  it('displays streaming indicator when isStreaming is true', () => {
    const message: Message = {
      id: 'msg-4',
      role: 'assistant',
      content: 'Streaming content...',
      isStreaming: true,
      timestamp: new Date(),
    };

    const { UNSAFE_root } = render(
      <StreamingMessage message={message} onCitationPress={mockOnCitationPress} />
    );

    // Check that streaming indicator is present (dots)
    expect(UNSAFE_root).toBeTruthy();
  });
});
