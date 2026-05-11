// AgentTimeline - Displays the research workflow with agent status indicators

import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { AgentStatus } from '../../types/research';
import { AgentNode } from './AgentNode';

interface AgentTimelineProps {
  statuses: AgentStatus[];
  isVisible?: boolean;
}

export function AgentTimeline({ statuses, isVisible = true }: AgentTimelineProps) {
  if (!isVisible || statuses.length === 0) return null;

  // Check if any agent is active or completed
  const hasActivity = statuses.some((s) => s.status !== 'pending');

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Research Workflow</Text>
        {hasActivity && (
          <View style={styles.activityIndicator}>
            <View style={styles.activityDot} />
            <Text style={styles.activityText}>In Progress</Text>
          </View>
        )}
      </View>

      {/* Timeline */}
      <ScrollView
        style={styles.timeline}
        contentContainerStyle={styles.timelineContent}
        showsVerticalScrollIndicator={false}
      >
        {statuses.map((status, index) => (
          <AgentNode key={`${status.agent}-${index}`} status={status} />
        ))}
      </ScrollView>

      {/* Footer hint */}
      {!hasActivity && (
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Submit a query to watch the multi-agent research workflow execute
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FDFCFB', // surface
    borderWidth: 1,
    borderColor: '#D1CCC4', // neutral-200
    borderRadius: 4,
    overflow: 'hidden',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#D1CCC4', // neutral-200
    backgroundColor: 'rgba(212, 165, 116, 0.04)', // primary-500 subtle tint
  },
  headerTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#0F0D0A', // neutral-900
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  activityIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 4,
    paddingHorizontal: 10,
    backgroundColor: 'rgba(124, 152, 133, 0.12)', // success-500 tint
    borderRadius: 12,
  },
  activityDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#7C9885', // success-500
  },
  activityText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#5A7A65', // success-600
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  timeline: {
    maxHeight: 400,
  },
  timelineContent: {
    padding: 16,
    paddingTop: 20,
  },
  footer: {
    padding: 16,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#D1CCC4', // neutral-200
    backgroundColor: 'rgba(155, 147, 136, 0.04)', // neutral-300 subtle tint
  },
  footerText: {
    fontSize: 12,
    color: '#6B6358', // neutral-500
    fontStyle: 'italic',
    textAlign: 'center',
    lineHeight: 18,
  },
});
