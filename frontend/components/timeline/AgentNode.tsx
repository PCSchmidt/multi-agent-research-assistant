// AgentNode - Individual agent status indicator in timeline

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { AgentStatus } from '../../types/research';

interface AgentNodeProps {
  status: AgentStatus;
}

// Agent-specific styling and labels
const AGENT_CONFIG = {
  search_s2: {
    label: 'Semantic Scholar',
    symbol: '🔍',
    color: '#8B7355', // Sienna (archaeological dig)
    description: 'Searching recent papers (2022-2024)',
  },
  search_arxiv: {
    label: 'arXiv',
    symbol: '📄',
    color: '#7B68A6', // Amethyst (hypothesis, ancient wisdom)
    description: 'Searching preprints and technical reports',
  },
  search_local: {
    label: 'Local Corpus',
    symbol: '📚',
    color: '#6B5334', // Deep bronze (foundational works)
    description: 'Searching canonical papers',
  },
  synthesize: {
    label: 'Synthesis',
    symbol: '∞',
    color: '#7C9885', // Verdigris (connections forming)
    description: 'Generating cited answer',
  },
  evaluate: {
    label: 'Evaluation',
    symbol: '⚖',
    color: '#C9A961', // Gold (measurement authority)
    description: 'Computing quality metrics',
  },
};

export function AgentNode({ status }: AgentNodeProps) {
  const config = AGENT_CONFIG[status.agent];
  const isPending = status.status === 'pending';
  const isActive = status.status === 'active';
  const isCompleted = status.status === 'completed';
  const isFailed = status.status === 'failed';

  return (
    <View style={styles.nodeContainer}>
      {/* Status indicator line */}
      <View style={styles.timelineColumn}>
        <View
          style={[
            styles.statusDot,
            { backgroundColor: config.color },
            isPending && styles.statusDotPending,
            isActive && styles.statusDotActive,
            isFailed && styles.statusDotFailed,
          ]}
        />
        {/* Connecting line (except for last item) */}
        <View
          style={[
            styles.connectingLine,
            { backgroundColor: isCompleted || isActive ? config.color : '#D1CCC4' },
            isPending && styles.connectingLinePending,
          ]}
        />
      </View>

      {/* Content */}
      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.symbol}>{config.symbol}</Text>
          <View style={styles.headerText}>
            <Text style={[styles.label, isPending && styles.labelPending]}>{config.label}</Text>
            <Text style={[styles.description, isPending && styles.descriptionPending]}>
              {config.description}
            </Text>
          </View>
        </View>

        {/* Status badge */}
        <View style={[styles.statusBadge, { borderColor: config.color }]}>
          <View
            style={[
              styles.statusBadgeIndicator,
              { backgroundColor: config.color },
              isPending && styles.statusBadgeIndicatorPending,
              isFailed && styles.statusBadgeIndicatorFailed,
            ]}
          />
          <Text
            style={[
              styles.statusBadgeText,
              { color: config.color },
              isPending && styles.statusBadgeTextPending,
            ]}
          >
            {status.status.toUpperCase()}
          </Text>
        </View>

        {/* Timestamp (if available) */}
        {status.timestamp && (
          <Text style={styles.timestamp}>
            {status.timestamp.toLocaleTimeString('en-US', {
              hour: 'numeric',
              minute: '2-digit',
              second: '2-digit',
              hour12: true,
            })}
          </Text>
        )}

        {/* Metadata (if available) */}
        {status.metadata && Object.keys(status.metadata).length > 0 && (
          <View style={styles.metadata}>
            {Object.entries(status.metadata).map(([key, value]) => (
              <Text key={key} style={styles.metadataText}>
                {key}: {String(value)}
              </Text>
            ))}
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  nodeContainer: {
    flexDirection: 'row',
    gap: 16,
  },
  timelineColumn: {
    alignItems: 'center',
    width: 24,
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    borderWidth: 2,
    borderColor: '#FDFCFB', // surface
  },
  statusDotPending: {
    opacity: 0.3,
  },
  statusDotActive: {
    width: 16,
    height: 16,
    borderRadius: 8,
    borderWidth: 3,
  },
  statusDotFailed: {
    backgroundColor: '#A05A52', // error-500
  },
  connectingLine: {
    flex: 1,
    width: 2,
    marginTop: 4,
  },
  connectingLinePending: {
    opacity: 0.2,
  },
  content: {
    flex: 1,
    paddingBottom: 24,
    gap: 8,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  symbol: {
    fontSize: 24,
    lineHeight: 28,
  },
  headerText: {
    flex: 1,
    gap: 4,
  },
  label: {
    fontSize: 16,
    fontWeight: '500',
    color: '#0F0D0A', // neutral-900
  },
  labelPending: {
    color: '#9B9388', // neutral-300
  },
  description: {
    fontSize: 13,
    color: '#6B6358', // neutral-500
    lineHeight: 18,
  },
  descriptionPending: {
    color: '#9B9388', // neutral-300
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: 6,
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
  },
  statusBadgeIndicator: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  statusBadgeIndicatorPending: {
    opacity: 0.3,
  },
  statusBadgeIndicatorFailed: {
    backgroundColor: '#A05A52', // error-500
  },
  statusBadgeText: {
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  statusBadgeTextPending: {
    color: '#9B9388', // neutral-300
  },
  timestamp: {
    fontSize: 11,
    color: '#9B9388', // neutral-300
    fontStyle: 'italic',
  },
  metadata: {
    marginTop: 4,
    paddingLeft: 12,
    borderLeftWidth: 2,
    borderLeftColor: '#D1CCC4', // neutral-200
    gap: 2,
  },
  metadataText: {
    fontSize: 11,
    color: '#6B6358', // neutral-500
    fontFamily: 'monospace',
  },
});
