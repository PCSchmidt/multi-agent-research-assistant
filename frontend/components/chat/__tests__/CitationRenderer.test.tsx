import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { CitationRenderer } from '../CitationRenderer';
import { Citation } from '../../../types/research';

describe('CitationRenderer', () => {
  const mockCitation: Citation = {
    number: 1,
    paperId: 'test-paper-id',
    relevanceScore: 0.95,
  };

  const mockOnPress = jest.fn();

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders citation number correctly', () => {
    const { getByText } = render(
      <CitationRenderer citation={mockCitation} onPress={mockOnPress} />
    );

    expect(getByText('[1]')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const { getByText } = render(
      <CitationRenderer citation={mockCitation} onPress={mockOnPress} />
    );

    fireEvent.press(getByText('[1]'));
    expect(mockOnPress).toHaveBeenCalledWith(mockCitation);
    expect(mockOnPress).toHaveBeenCalledTimes(1);
  });

  it('renders different citation numbers', () => {
    const citation2 = { ...mockCitation, number: 42 };
    const { getByText } = render(
      <CitationRenderer citation={citation2} onPress={mockOnPress} />
    );

    expect(getByText('[42]')).toBeTruthy();
  });
});
