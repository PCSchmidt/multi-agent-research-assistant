import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { Link } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function SignupScreen() {
  return (
    <View style={styles.container}>
      <StatusBar style="dark" />

      <View style={styles.content}>
        <Text style={styles.title}>Create Account</Text>
        <Text style={styles.subtitle}>Join the scholarly archive</Text>

        <View style={styles.form}>
          <TextInput
            style={styles.input}
            placeholder="Email"
            placeholderTextColor="#6B6358"
            autoCapitalize="none"
            keyboardType="email-address"
          />

          <TextInput
            style={styles.input}
            placeholder="Password"
            placeholderTextColor="#6B6358"
            secureTextEntry
          />

          <TextInput
            style={styles.input}
            placeholder="Confirm Password"
            placeholderTextColor="#6B6358"
            secureTextEntry
          />

          <TouchableOpacity style={styles.primaryButton}>
            <Text style={styles.primaryButtonText}>Create Account</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Already have an account? </Text>
          <Link href="/(auth)/login" asChild>
            <TouchableOpacity>
              <Text style={styles.linkTextBold}>Sign In</Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F3F0',
  },
  content: {
    flex: 1,
    paddingHorizontal: 32,
    paddingTop: 80,
  },
  title: {
    fontSize: 40,
    fontWeight: '400',
    color: '#0F0D0A',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#6B6358',
    marginBottom: 48,
  },
  form: {
    gap: 16,
  },
  input: {
    backgroundColor: '#FDFCFB',
    borderWidth: 1,
    borderColor: '#D1CCC4',
    borderBottomWidth: 2,
    borderBottomColor: '#9B9388',
    borderRadius: 2,
    padding: 16,
    fontSize: 16,
    color: '#0F0D0A',
  },
  primaryButton: {
    backgroundColor: '#D4A574',
    borderWidth: 1,
    borderColor: 'rgba(107, 83, 52, 0.3)',
    borderRadius: 2,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  primaryButtonText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#0F0D0A',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 32,
  },
  footerText: {
    fontSize: 14,
    color: '#6B6358',
  },
  linkTextBold: {
    fontSize: 14,
    color: '#B8935F',
    fontWeight: '600',
  },
});
