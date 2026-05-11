import React from 'react';
import { render } from '@testing-library/react-native';
import { AgentNode } from '../AgentNode';
import { AgentStatus } from '../../../types/research';

describe('AgentNode', () => {
  it('renders pending status correctly', () => {
    const status: AgentStatus = {
      agent: 'search_s2',
      status: 'pending',
    };

    const { getByText } = render(<AgentNode status={status} />);

    expect(getByText('Semantic Scholar')).toBeTruthy();
    expect(getByText('Searching recent papers (2022-2024)')).toBeTruthy();
    expect(getByText('PENDING')).toBeTruthy();
  });

  it('renders completed status with metadata', () => {
    const status: AgentStatus = {
      agent: 'synthesize',
      status: 'completed',
      timestamp: new Date('2024-01-01T12:00:00'),
      metadata: { tokensGenerated: 487, citationsAdded: 4 },
    };

    const { getByText } = render(<AgentNode status={status} />);

    expect(getByText('Synthesis')).toBeTruthy();
    expect(getByText('COMPLETED')).toBeTruthy();
    expect(getByText('tokensGenerated: 487')).toBeTruthy();
    expect(getByText('citationsAdded: 4')).toBeTruthy();
  });

  it('renders all agent types correctly', () => {
    const agents: AgentStatus['agent'][] = [
      'search_s2',
      'search_arxiv',
      'search_local',
      'synthesize',
      'evaluate',
    ];

    const expectedLabels = [
      'Semantic Scholar',
      'arXiv',
      'Local Corpus',
      'Synthesis',
      'Evaluation',
    ];

    agents.forEach((agent, index) => {
      const status: AgentStatus = { agent, status: 'active' };
      const { getByText } = render(<AgentNode status={status} />);
      expect(getByText(expectedLabels[index])).toBeTruthy();
    });
  });

  it('renders failed status correctly', () => {
    const status: AgentStatus = {
      agent: 'evaluate',
      status: 'failed',
    };

    const { getByText } = render(<AgentNode status={status} />);

    expect(getByText('FAILED')).toBeTruthy();
  });
});
