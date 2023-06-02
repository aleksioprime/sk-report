import { ref, onMounted, computed } from 'vue'
import { axiosAPI } from '@/axios'


// В массиве полей в конце нужно указывать id, если это необходимо
export function getGroupedArray() {
	function groupedArrayData (array, fields) {
		let groupedObject = array.reduce((acc, obj) => {
		  let objField = obj
		  for (const field of fields) {
			objField = objField[field];
		  }
		  const property = objField;
		  acc[property] = acc[property] || [];
		  acc[property].push(obj);
		  return acc;
		}, {});
		return groupedObject;
	  }
	return  {
		groupedArrayData
	}
}