export function validateValue(value, rules = []) {
    for (const rule of rules) {
      if (rule.type === 'required' && !value) {
        return rule.message || 'This field is required.'
      }
      if (rule.type === 'minLength' && value.length < rule.value) {
        return rule.message || `Minimum length is ${rule.value}`
      }
      // ... أكمل باقي الشروط
    }
    return null
  }
  