
const payload = {
  id: 30,
  title: "تقديم جامعة حلوان الأهلية",
  is_active: true,
  created_at: "2025-05-06T18:12:12.783961+03:00",
  modified_at: "2025-05-06 19:22",
  tabs: [
    {
      id: 109,
      title: "البيانات الأساسية",
      order: 1,
      sections: [
        {
          id: 107,
          title: "البيانات الأساسية",
          order: 1,
          questions: [
            {
              id: 185,
              title: "الاسم رباعي باللغة العربية",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                  {
                    type: "regex",
                    value:
                      "^(?!\\s)(?!.*\\d)(?!.*[A-Za-z])(?!.*[^\\u0600-\\u06FF\\s])(?:.*\\s){3,}.*(?<!\\s)$",
                    message: "",
                  },
                ],
                placeholder: "الاسم رباعي باللغة العربية",
              },
              order: 1,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 186,
              title: "الاسم رباعي باللغة الانجليزية",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                  {
                    type: "regex",
                    value:
                      "^(?!\\s)(?!.*\\d)(?!.*[\\u0600-\\u06FF])(?!.*[^A-Za-z\\s])(?:.*\\s){3,}.*(?<!\\s)$",
                    message: "",
                  },
                ],
                placeholder: "الاسم رباعي باللغة الانجليزية",
              },
              order: 2,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 187,
              title: "النوع",
              question_type: "select",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
              },
              order: 3,
              options: [
                {
                  id: 83,
                  title: "ذكر",
                  order: 1,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 84,
                  title: "انثى",
                  order: 2,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
              ],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 188,
              title: "الرقم القومي",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "regex",
                    value:
                      "^(2|3)\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\\d{7}$",
                    message: "",
                  },
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                placeholder: "ادخل الرقم القومي المصري المكون من 14 رقم",
              },
              order: 4,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 189,
              title: "رقم موبايل الطالب",
              question_type: "text",
              is_required: false,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                placeholder: "رقم موبايل الطالب",
              },
              order: 5,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 190,
              title: "رقم موبايل ولي الأمر",
              question_type: "text",
              is_required: false,
              configs: {
                rules: [],
                placeholder: "رقم موبايل ولي الأمر",
              },
              order: 5,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 191,
              title: "الشهادة",
              question_type: "select",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
              },
              order: 7,
              options: [
                {
                  id: 85,
                  title: "الثانوية العامة المصرية",
                  order: 1,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 86,
                  title: "الشهادات المعادلة العربية",
                  order: 2,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 87,
                  title: "الشهادات المعادلة الأجنبية",
                  order: 3,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 88,
                  title: "الثانوية الأزهرية",
                  order: 4,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 89,
                  title: "شهادة النيل",
                  order: 5,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 90,
                  title: "مدارس المتفوقين STEM",
                  order: 6,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
              ],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 192,
              title: "سنة الحصول على الشهادة",
              question_type: "select",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
              },
              order: 8,
              options: [
                {
                  id: 91,
                  title: "2024",
                  order: 1,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 92,
                  title: "2025",
                  order: 2,
                  meta_data: {
                    rules: [],
                    type_of_rules: "number",
                    is_locked: false,
                  },
                  is_archived: false,
                },
              ],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
          ],
          meta_data: {},
          is_archived: false,
        },
      ],
      meta_data: {
        depend_question: "",
      },
      is_archived: false,
    },
    {
      id: 110,
      title: "نوع الشهادة",
      order: 2,
      sections: [
        {
          id: 108,
          title: "نوع الشهادة",
          order: 1,
          questions: [
            {
              id: 193,
              title: "نوع الشهادة",
              question_type: "select",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                placeholder: "نوع الشهادة",
              },
              order: 1,
              options: [
                {
                  id: 93,
                  title: "علمي علوم - 2024",
                  order: 1,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 94,
                  title: "علمي علوم - 2025",
                  order: 2,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 95,
                  title: "علمي رياضة- 2024",
                  order: 3,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 96,
                  title: "علمي رياضة- 2025",
                  order: 4,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 97,
                  title: "ادبي - 2024",
                  order: 5,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 99,
                  title: "ادبي - 2025",
                  order: 6,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية العامة المصرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 100,
                  title: "معادلة عربية - علمي - 2024",
                  order: 7,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة العربية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 101,
                  title: "معادلة عربية - علمي - 2025",
                  order: 8,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة العربية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 102,
                  title: "معادلة عربية - ادبي - 2024",
                  order: 9,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة العربية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 103,
                  title: "معادلة عربية - ادبي - 2025",
                  order: 10,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة العربية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 104,
                  title: "معادلة أجنبية - 2024",
                  order: 11,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة الأجنبية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 105,
                  title: "معادلة أجنبية - 2025",
                  order: 12,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الشهادات المعادلة الأجنبية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 106,
                  title: "ازهري - علمي - 2024",
                  order: 13,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية الأزهرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 107,
                  title: "ازهري - علمي - 2025",
                  order: 14,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية الأزهرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 108,
                  title: "ازهري - أدبي - 2024",
                  order: 15,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية الأزهرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 109,
                  title: "ازهري - أدبي - 2025",
                  order: 16,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "الثانوية الأزهرية",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 110,
                  title: "النيل - 2024",
                  order: 17,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "شهادة النيل",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 111,
                  title: "النيل - 2025",
                  order: 18,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "شهادة النيل",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 112,
                  title: "STEM - 2024",
                  order: 19,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "مدارس المتفوقين STEM",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
                {
                  id: 113,
                  title: "STEM - 2025",
                  order: 20,
                  meta_data: {
                    rules: [
                      {
                        type: "equal",
                        value: "مدارس المتفوقين STEM",
                        message: "",
                      },
                    ],
                    type_of_rules: "text",
                    is_locked: false,
                  },
                  is_archived: false,
                },
              ],
              is_archived: false,
              meta_data: {
                depend_question: {
                  name: "البيانات الأساسية | البيانات الأساسية | الشهادة",
                  code: "البيانات الأساسية | البيانات الأساسية | الشهادة",
                },
                description: "",
              },
            },
          ],
          meta_data: {},
          is_archived: false,
        },
      ],
      meta_data: {
        depend_question: null,
      },
      is_archived: false,
    },
    {
      id: 111,
      title: "البيانات الأكاديمية",
      order: 3,
      sections: [
        {
          id: 109,
          title: "علمي - 2024",
          order: 1,
          questions: [
            {
              id: 194,
              title: "رقم الجلوس",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
              },
              order: 1,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 195,
              title: "المجموع بالأرقام",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "regex",
                    value:
                      "^(?:410(?:\\.0|\\.5)?|(?:[0-9]{1,2}|[1-3][0-9]{1,2})(?:\\.0|\\.5)?)$",
                    message: "المجموع خاطئ",
                  },
                ],
                placeholder: "اكتب المجموع بالأرقام كما بالشهادة",
              },
              order: 2,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 196,
              title: "النسبة المئوية",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "regex",
                    value: "^(5[3-9]|[6-9][0-9]|100)$",
                    message: "انسبة تتراوح بين 53 الى 100 فقط",
                  },
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                placeholder: "اكتب النسبة مثال 57.22",
              },
              order: 3,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 197,
              title: "صورة شهادة الثانوية العامة",
              question_type: "file-upload",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                maxSize: 50,
                fileTypes:
                  "image/png,image/jpeg,image/jpg,image/webp,image/gif,application/pdf",
                maxFiles: 1,
              },
              order: 4,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
          ],
          meta_data: {},
          is_archived: false,
        },
        {
          id: 110,
          title: "علمي - 2025",
          order: 1,
          questions: [
            {
              id: 194,
              title: "رقم الجلوس",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
              },
              order: 1,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 195,
              title: "المجموع بالأرقام",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "regex",
                    value:
                      "^(?:410(?:\\.0|\\.5)?|(?:[0-9]{1,2}|[1-3][0-9]{1,2})(?:\\.0|\\.5)?)$",
                    message: "المجموع خاطئ",
                  },
                ],
                placeholder: "اكتب المجموع بالأرقام كما بالشهادة",
              },
              order: 2,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 196,
              title: "النسبة المئوية",
              question_type: "text",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "regex",
                    value: "^(5[3-9]|[6-9][0-9]|100)$",
                    message: "انسبة تتراوح بين 53 الى 100 فقط",
                  },
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                placeholder: "اكتب النسبة مثال 57.22",
              },
              order: 3,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
            {
              id: 197,
              title: "صورة شهادة الثانوية العامة",
              question_type: "file-upload",
              is_required: true,
              configs: {
                rules: [
                  {
                    type: "required",
                    value: "",
                    message: "",
                  },
                ],
                maxSize: 50,
                fileTypes:
                  "image/png,image/jpeg,image/jpg,image/webp,image/gif,application/pdf",
                maxFiles: 1,
              },
              order: 4,
              options: [],
              is_archived: false,
              meta_data: {
                depend_question: "",
                description: "",
              },
            },
          ],
          meta_data: {},
          is_archived: false,
        },
      ],
      meta_data: {
        depend_question: {
          name: "نوع الشهادة | نوع الشهادة | نوع الشهادة",
          code: "نوع الشهادة | نوع الشهادة | نوع الشهادة",
        },
      },
      is_archived: false,
    },
  ],
  meta_data: {
    description: "",
    date_start: "",
    date_end: "",
    submissonsCount: 100000,
    userSubmitCount: 1,
    ignore_date: false,
  },
  submissions_count: 1,
};

axios
  .put("http://admission.hnu.edu.eg:81/api/admissions/forms/30", payload, {
    headers: {
      "Content-Type": "application/json",
      // 'Authorization': 'Bearer YOUR_TOKEN' // لو محتاج توكن
    },
  })
  .then((res) => {
    // console.log("تم الإرسال بنجاح:", res.data);
  })
  .catch((err) => {
    // console.error("حدث خطأ أثناء الإرسال:", err.response?.data || err);
  });
