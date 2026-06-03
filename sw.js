self.addEventListener('install',function(){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});
self.addEventListener('notificationclick',function(e){
  e.notification.close();
  e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(function(cl){
    for(var i=0;i<cl.length;i++){if(cl[i].url.indexOf('peptideos-pro')>=0)return cl[i].focus();}
    return self.clients.openWindow('/peptideos-pro/');
  }));
});
self.addEventListener('periodicsync',function(e){
  if(e.tag==='daily-dose'){
    e.waitUntil(self.registration.showNotification('PeptideOS Pro',{
      body:"Time for your daily peptides! Open the app to log today's doses.",
      tag:'daily-dose',requireInteraction:true
    }));
  }
});