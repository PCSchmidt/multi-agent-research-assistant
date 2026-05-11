// Mock data for v0.3/v0.4 - Academic Research Assistant UI

import { Paper, Message, EvalScores, AgentStatus } from '../types/research';

export const mockPapers: Paper[] = [
  {
    id: '1',
    paperId: '204e3073870fae3d05bcbc2f6a8e263d9b72e776',
    title: 'Attention Is All You Need',
    authors: [
      { name: 'Ashish Vaswani', authorId: '2143158538' },
      { name: 'Noam Shazeer' },
      { name: 'Niki Parmar' },
      { name: 'Jakob Uszkoreit' },
      { name: 'Llion Jones' },
      { name: 'Aidan N. Gomez' },
      { name: 'Lukasz Kaiser' },
      { name: 'Illia Polosukhin' },
    ],
    abstract:
      'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.',
    year: 2017,
    venue: 'NIPS',
    citationCount: 87234,
    url: 'https://arxiv.org/abs/1706.03762',
    source: 'local',
  },
  {
    id: '2',
    paperId: 'a16c597c3e66e3f4c46e04280d2d1fbf9bbd3b2d',
    title: 'Longformer: The Long-Document Transformer',
    authors: [
      { name: 'Iz Beltagy' },
      { name: 'Matthew E. Peters' },
      { name: 'Arman Cohan' },
    ],
    abstract:
      'Transformer-based models are unable to process long sequences due to their self-attention operation, which scales quadratically with the sequence length. To address this limitation, we introduce the Longformer with an attention mechanism that scales linearly with sequence length, making it easy to process documents of thousands of tokens or longer. Longformer\'s attention mechanism is a drop-in replacement for the standard self-attention and combines a local windowed attention with a task motivated global attention.',
    year: 2020,
    venue: 'arXiv',
    citationCount: 1842,
    url: 'https://arxiv.org/abs/2004.05150',
    source: 'arxiv',
  },
  {
    id: '3',
    paperId: '9e9ca74c8a8f4d8e8e5b7c8d9e0f1a2b3c4d5e6f',
    title: 'Efficient Attention: Attention with Linear Complexities',
    authors: [
      { name: 'Zhuoran Shen' },
      { name: 'Mingyuan Zhang' },
      { name: 'Haiyu Zhao' },
      { name: 'Shuai Yi' },
      { name: 'Hongsheng Li' },
    ],
    abstract:
      'Dot-product attention has quadratic complexity with respect to the sequence length, which is a significant limitation for long sequences. We propose Efficient Attention, a novel attention mechanism that achieves linear complexity by using kernel feature maps to approximate the softmax operation. Our method can be used as a drop-in replacement for standard attention in Transformer models.',
    year: 2021,
    venue: 'WACV',
    citationCount: 342,
    url: 'https://arxiv.org/abs/1812.01243',
    source: 's2',
  },
  {
    id: '4',
    paperId: '7f8e9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f',
    title: 'Reformer: The Efficient Transformer',
    authors: [
      { name: 'Nikita Kitaev' },
      { name: 'Łukasz Kaiser' },
      { name: 'Anselm Levskaya' },
    ],
    abstract:
      'Large Transformer models are increasingly used for natural language processing tasks, but they have significant computational and memory requirements. We introduce the Reformer, which uses locality-sensitive hashing to reduce the complexity of attention from O(L^2) to O(L log L), where L is the sequence length. We also use reversible residual layers to reduce memory consumption during training.',
    year: 2020,
    venue: 'ICLR',
    citationCount: 1456,
    url: 'https://arxiv.org/abs/2001.04451',
    source: 's2',
  },
];

export const mockEvalScores: EvalScores = {
  faithfulness: 0.87,
  answerRelevancy: 0.92,
  contextPrecision: 0.78,
  citationAccuracy: 0.85,
  recencyScore: 0.73,
  coverageScore: 0.89,
  status: 'completed',
};

export const mockAgentStatuses: AgentStatus[] = [
  {
    agent: 'search_s2',
    status: 'completed',
    timestamp: new Date(Date.now() - 3.5 * 60 * 1000),
    metadata: { papersFound: 12, filtered: 3 },
  },
  {
    agent: 'search_arxiv',
    status: 'completed',
    timestamp: new Date(Date.now() - 3.3 * 60 * 1000),
    metadata: { papersFound: 8, filtered: 1 },
  },
  {
    agent: 'search_local',
    status: 'completed',
    timestamp: new Date(Date.now() - 3.1 * 60 * 1000),
    metadata: { papersFound: 5, filtered: 1 },
  },
  {
    agent: 'synthesize',
    status: 'completed',
    timestamp: new Date(Date.now() - 2.9 * 60 * 1000),
    metadata: { tokensGenerated: 487, citationsAdded: 4 },
  },
  {
    agent: 'evaluate',
    status: 'completed',
    timestamp: new Date(Date.now() - 2.7 * 60 * 1000),
    metadata: { metricsComputed: 6 },
  },
];

export const mockAgentStatusesPending: AgentStatus[] = [
  {
    agent: 'search_s2',
    status: 'pending',
  },
  {
    agent: 'search_arxiv',
    status: 'pending',
  },
  {
    agent: 'search_local',
    status: 'pending',
  },
  {
    agent: 'synthesize',
    status: 'pending',
  },
  {
    agent: 'evaluate',
    status: 'pending',
  },
];

export const mockMessages: Message[] = [
  {
    id: 'msg-1',
    role: 'user',
    content: 'What are the main approaches to reducing the computational complexity of attention mechanisms in transformers?',
    timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
  },
  {
    id: 'msg-2',
    role: 'assistant',
    content:
      'Based on recent research, there are several key approaches to reducing the quadratic complexity of attention mechanisms in transformers:\n\n**1. Sparse Attention Patterns**\nThe Longformer [1] introduces a windowed attention mechanism that combines local attention with task-specific global attention, achieving linear complexity with respect to sequence length. This allows processing of documents with thousands of tokens without the memory constraints of standard transformers.\n\n**2. Kernel-Based Approximations**\nEfficient Attention [2] proposes using kernel feature maps to approximate the softmax operation in attention, reducing complexity from O(L²) to O(L). This approach treats attention as a kernel operation and can be used as a drop-in replacement in existing architectures.\n\n**3. Locality-Sensitive Hashing**\nThe Reformer [3] uses LSH to group similar queries and keys together, reducing the number of attention computations required. Combined with reversible residual layers, this approach significantly reduces both computational and memory requirements.\n\n**4. Foundational Architecture**\nAll of these methods build upon the original Transformer architecture [4], which established the self-attention mechanism as a core component of modern NLP models.\n\nThese approaches demonstrate that the quadratic scaling of attention is not fundamental, and various approximations can maintain model quality while dramatically improving efficiency for long sequences.',
    citations: [
      { number: 1, paperId: '2', relevanceScore: 0.94 },
      { number: 2, paperId: '3', relevanceScore: 0.89 },
      { number: 3, paperId: '4', relevanceScore: 0.92 },
      { number: 4, paperId: '1', relevanceScore: 0.97 },
    ],
    papers: mockPapers,
    evalScores: mockEvalScores,
    agentStatuses: mockAgentStatuses,
    timestamp: new Date(Date.now() - 4 * 60 * 1000), // 4 minutes ago
  },
];

export const streamingMessageContent = 'Based on recent research, there are several key approaches to reducing the quadratic complexity of attention mechanisms in transformers:\n\n**1. Sparse Attention Patterns**\nThe Longformer [1] introduces a windowed attention mechanism that combines local attention with task-specific global attention, achieving linear complexity with respect to sequence length.';
