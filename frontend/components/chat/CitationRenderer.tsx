// CitationRenderer - Displays citation numbers as tappable superscripts

import React from 'react';
import { Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Citation } from '../../types/research';

interface CitationRendererProps {
  citation: Citation;
  onPress: (citation: Citation) => void;
}

export function CitationRenderer({ citation, onPress }: CitationRendererProps) {
  return (
    <TouchableOpacity
      onPress={() => onPress(citation)}
      style={styles.citationContainer}
      activeOpacity={0.6}
    >
      <Text style={styles.citationText}>[{citation.number}]</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  citationContainer: {
    paddingHorizontal: 2,
  },
  citationText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#B8935F', // primary-600 (link color)
    textDecorationLine: 'underline',
    textDecorationStyle: 'solid',
    textDecorationColor: '#B8935F',
    lineHeight: 14,
  },
});
