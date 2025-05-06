// validation.js

export function validateValue(value, rules = [], type = 'text') {
  for (const rule of rules) {
    const val = rule.value

    // 🟥 النصوص و Textarea
    if (["text", "textarea"].includes(type)) {
      if (rule.type === 'required' && (!value || value.trim() === '')) {
        return rule.message || 'هذا الحقل مطلوب'
      }
      if (rule.type === 'equal' && (value !== val)) {
        return rule.message || 'قيمة خاطئة'
      }
      if (rule.type === 'minLength' && value.length < val) {
        return rule.message || `يجب ألا يقل عن ${val} حرفًا`
      }
      if (rule.type === 'maxLength' && value.length > val) {
        return rule.message || `يجب ألا يزيد عن ${val} حرفًا`
      }
      if (rule.type === 'regex') {
        try {
          const regex = new RegExp(val)
          if (!regex.test(value)) return rule.message || 'الصيغة غير صحيحة'
        } catch {
          return 'صيغة Regex غير صالحة'
        }
      }
    }

    // 🔢 الأرقام
    if (type === 'number') {
      // console.log(`validation : ${JSON.stringify(type, null, 2)}`);
      const num = Number(value)
      // console.log(`validation val1 : ${num}`);
      // console.log(`validation rule.type : ${rule.type}`);
      // console.log(`validation val2 : ${val}`);

      if (rule.type === 'required' && (value === '' || isNaN(num))) {
        return rule.message || 'هذا الحقل مطلوب'
      }
      if (rule.type === 'minLength' && String(num).length < val) {
        return rule.message || `عدد الأرقام أقل من ${val}`
      }
      if (rule.type === 'maxLength' && String(num).length > val) {
        return rule.message || `عدد الأرقام أكثر من ${val}`
      }
      if (rule.type === 'min' && num < val) {
        return rule.message || `يجب أن يكون أكبر من ${val}`
      }
      if (rule.type === 'max' && num > val) {
        return rule.message || `يجب أن يكون أقل من ${val}`
      }
      if (rule.type === 'max_eq' && num < val) {
        return rule.message || `يجب أن يكون أكبر من أو يساوي ${val}`
      }
      if (rule.type === 'min_eq' && num > val) {
        return rule.message || `يجب أن يكون أقل من أو يساوي ${val}`
      }
      if (rule.type === 'not_eq' && num == val) {
        return rule.message || `يجب ألا يكون ${val}`
      }
      if (rule.type === 'regex') {
        try {
          const regex = new RegExp(val)
          if (!regex.test(value)) return rule.message || 'الصيغة غير صحيحة'
        } catch {
          return 'صيغة Regex غير صالحة'
        }
      }
    }

    // 📎 الملفات
    if (type === 'file-upload') {
      if (rule.type === 'required' && !value) {
        return rule.message || 'الملف مطلوب'
      }
      if (rule.type === 'maxSize' && value?.size / (1024 * 1024) > val) {
        return rule.message || `يجب ألا يزيد حجم الملف عن ${val}MB`
      }
      if (rule.type === 'types' && value?.type && !val.split(',').includes(value.type)) {
        return rule.message || `نوع الملف غير مدعوم: ${value.type}`
      }
    }

    // ✅ التحقق من اختيارات متعددة (checkbox, draggable)
    if (["checkbox", "draggable"].includes(type)) {
      const len = Array.isArray(value) ? value.length : 0
      if (rule.type === 'required' && len === 0) {
        return rule.message || 'اختر عنصرًا واحدًا على الأقل'
      }
      if (rule.type === 'min' && len < val) {
        return rule.message || `يجب اختيار على الأقل ${val}`
      }
      if (rule.type === 'max' && len > val) {
        return rule.message || `يمكنك اختيار حتى ${val}`
      }
      if (rule.type === 'equal' && len != val) {
        return rule.message || `يجب اختيار عدد مساوي لـ ${val} `
      }
    }

    // 🔘 radio, select, payment
    if (["radio", "select", "payment"].includes(type)) {
      if (rule.type === 'required' && (!value || value === '')) {
        return rule.message || 'هذا الحقل مطلوب'
      }
    }

    // 🗓 التاريخ
    if (type === 'date') {
      const inputDate = new Date(value)
      if (rule.type === 'required' && !value) {
        return rule.message || 'يرجى إدخال تاريخ'
      }
      if (rule.type === 'minDate' && new Date(val) > inputDate) {
        return rule.message || `التاريخ يجب أن يكون بعد ${val}`
      }
      if (rule.type === 'maxDate' && new Date(val) < inputDate) {
        return rule.message || `التاريخ يجب أن يكون قبل ${val}`
      }
    }
  }

  return null // ✅ valid
}
