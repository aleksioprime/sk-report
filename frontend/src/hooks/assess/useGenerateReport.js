import axios from 'axios'
import { ref, onMounted } from 'vue'

export function getChatGPTReport() {
	const generatedGPTText = ref([]);
  const isGPTTextLoading = ref(false);
	const fetchChatGPTReport = async (info) => {
    console.log(info)
    const prompt = `Напиши отзыв о ${info.first_name}, который по предмету ${info.subject} получил слещующие оценки: 
    по критерию ${info.criteria.criterion_a.name_eng} - ${info.mark.criterion_a}, 
    по критерию ${info.criteria.criterion_b.name_eng} - ${info.mark.criterion_b}, 
    по критерию ${info.criteria.criterion_c.name_eng} - ${info.mark.criterion_с}, 
    по критерию ${info.criteria.criterion_d.name_eng} - ${info.mark.criterion_d}`;
		const apiKey = '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';
    const apiUrl = 'https://api.openai.com/v1/completions';
    const data = {
      prompt: prompt,
      model: "text-davinci-003",
      max_tokens: 1000, // Максимальное количество токенов в ответе
      temperature: 0.7, // Параметр, контролирующий "творчество" ответов (чем выше значение, тем более случайными будут ответы)
      n: 1, // Количество вариантов ответов, которые API вернет в ответе
    };
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }
    }
    isGPTTextLoading.value = true;
		await axios.post(apiUrl, data, config).then((response) => {
			console.log("Генерация текста")
      console.log(response.data)
      const { choices } = response.data;
      const [reply] = choices;
			generatedGPTText.value = reply.text.trim()
			console.log(generatedGPTText.value)
		}).finally(() => {
      isGPTTextLoading.value = false;
    });
	};
	return {
		generatedGPTText, isGPTTextLoading, fetchChatGPTReport
	}
}
