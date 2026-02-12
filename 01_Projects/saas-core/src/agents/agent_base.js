 



module.exports = {
name: "Agent Base",
role: "Asistente general del SaaS Factory",
goal: "Ayudar a ejecutar tareas de forma clara y ordenada",

run(task) {
if (!task) {
return "No me diste ninguna tarea.";
}

return `Tarea recibida: ${task}. Ejecutando... `;
  }
};
