// PaperDetailsPanel - Modal/bottom sheet showing paper metadata when citation is tapped

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  ScrollView,
  TouchableOpacity,
  Linking,
  Platform,
} from 'react-native';
import { Paper } from '../../types/research';

interface PaperDetailsPanelProps {
  paper: Paper | null;
  visible: boolean;
  onClose: () => void;
}

export function PaperDetailsPanel({ paper, visible, onClose }: PaperDetailsPanelProps) {
  if (!paper) return null;

  const handleOpenURL = () => {
    if (paper.url) {
      Linking.openURL(paper.url);
    }
  };

  const sourceLabel =
    paper.source === 's2'
      ? 'Semantic Scholar'
      : paper.source === 'arxiv'
      ? 'arXiv'
      : 'Local Corpus';

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.panel}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.headerTop}>
              <Text style={styles.sourceLabel}>{sourceLabel}</Text>
              <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                <Text style={styles.closeButtonText}>✕</Text>
              </TouchableOpacity>
            </View>
            <Text style={styles.title}>{paper.title}</Text>
          </View>

          {/* Content */}
          <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
            {/* Authors */}
            <View style={styles.section}>
              <Text style={styles.sectionLabel}>Authors</Text>
              <Text style={styles.authors}>
                {paper.authors.map((a) => a.name).join(', ')}
              </Text>
            </View>

            {/* Metadata */}
            <View style={styles.metadataRow}>
              <View style={styles.metadataItem}>
                <Text style={styles.metadataLabel}>Year</Text>
                <Text style={styles.metadataValue}>{paper.year}</Text>
              </View>
              <View style={styles.metadataItem}>
                <Text style={styles.metadataLabel}>Venue</Text>
                <Text style={styles.metadataValue}>{paper.venue}</Text>
              </View>
              <View style={styles.metadataItem}>
                <Text style={styles.metadataLabel}>Citations</Text>
                <Text style={styles.metadataValue}>{paper.citationCount.toLocaleString()}</Text>
              </View>
            </View>

            {/* Abstract */}
            <View style={styles.section}>
              <Text style={styles.sectionLabel}>Abstract</Text>
              <Text style={styles.abstract}>{paper.abstract}</Text>
            </View>

            {/* Link */}
            {paper.url && (
              <TouchableOpacity onPress={handleOpenURL} style={styles.linkButton}>
                <Text style={styles.linkButtonText}>View Full Paper →</Text>
              </TouchableOpacity>
            )}
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(15, 13, 10, 0.75)', // neutral-900 with opacity
    justifyContent: 'flex-end',
  },
  panel: {
    backgroundColor: '#FDFCFB', // surface
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
    maxHeight: '85%',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
      },
      android: {
        elevation: 8,
      },
    }),
  },
  header: {
    padding: 24,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#D1CCC4', // neutral-200
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sourceLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#D4A574', // primary-500
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  closeButton: {
    width: 32,
    height: 32,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 16,
    backgroundColor: '#F5F3F0', // neutral-50
  },
  closeButtonText: {
    fontSize: 18,
    color: '#6B6358', // neutral-500
    fontWeight: '400',
  },
  title: {
    fontSize: 20,
    fontWeight: '400',
    color: '#0F0D0A', // neutral-900
    lineHeight: 28,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 24,
    paddingTop: 20,
    gap: 20,
  },
  section: {
    gap: 8,
  },
  sectionLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6B6358', // neutral-500
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  authors: {
    fontSize: 15,
    color: '#0F0D0A', // neutral-900
    lineHeight: 22,
  },
  metadataRow: {
    flexDirection: 'row',
    gap: 24,
  },
  metadataItem: {
    gap: 4,
  },
  metadataLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: '#9B9388', // neutral-300
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  metadataValue: {
    fontSize: 15,
    fontWeight: '500',
    color: '#0F0D0A', // neutral-900
  },
  abstract: {
    fontSize: 15,
    color: '#3D3832', // neutral-700
    lineHeight: 24,
  },
  linkButton: {
    backgroundColor: 'rgba(212, 165, 116, 0.12)', // primary-500 tint
    borderWidth: 1,
    borderColor: '#D4A574', // primary-500
    borderRadius: 4,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  linkButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#B8935F', // primary-600
    letterSpacing: 0.5,
  },
});
