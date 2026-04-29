// ============================================================
// SITE CONFIG - AGIA 360 AI AGENCY
// ============================================================
// Configuración centralizada de la marca, servicios y equipo.
// ============================================================

export interface ServiceItem {
  icon: 'divorce' | 'custody' | 'alimony' | 'mediation' | 'domestic-violence' | 'separation' | 'contracts' | 'corporate' | 'real-estate' | 'criminal' | 'immigration' | 'labor' | 'custom'
  title: string
  slug: string
  shortDescription: string
  fullDescription: string
}

export interface TeamMember {
  name: string
  title: string
  bio: string
  specialties: string[]
  imageUrl?: string
  bookingSlug?: string
}

export interface Testimonial {
  name: string
  quote: string
  rating: number
  caseType?: string
}

export interface NavItem {
  label: string
  href: string
  children?: { label: string; href: string }[]
}

export interface SiteConfig {
  firmName: string
  firmSlogan: string
  firmDescription: string
  founderName: string
  founderTitle: string
  founderBio: string
  yearsExperience: number
  yearFounded: number

  contact: {
    phone: string
    phoneDisplay: string
    email: string
    address: string
    city: string
    country: string
    googleMapsEmbedUrl: string
    whatsappNumber?: string
    officeHours: string
  }

  social: {
    facebook?: string
    instagram?: string
    linkedin?: string
    twitter?: string
  }

  navigation: {
    items: NavItem[]
  }

  hero: {
    headline: string
    subheadline: string
    ctaText: string
    ctaHref: string
    backgroundImageUrl?: string
  }

  values: Array<{
    icon: 'respect' | 'quality' | 'team' | 'experience' | 'confidential' | 'results'
    title: string
    description: string
  }>

  services: ServiceItem[]

  tabs: Array<{
    title: string
    content: string
  }>

  team: TeamMember[]

  testimonials: Testimonial[]

  booking: {
    enabled: boolean
    ctaText: string
    mainLawyerSlug?: string
  }

  seo: {
    siteTitle: string
    titleTemplate: string
    defaultDescription: string
    locale: string
    ogImageUrl?: string
  }

  legal: {
    privacyLastUpdated: string
    termsLastUpdated: string
  }

  theme?: {
    primaryColor?: string
    accentColor?: string
  }
}

// ============================================================
// CONFIGURACIÓN DE INSTANCIA: AGIA 360
// ============================================================

export const siteConfig: SiteConfig = {
  firmName: 'Agia 360',
  firmSlogan: 'Transformación Inteligente para tu Negocio',
  firmDescription: 'Agencia de IA especializada en auditorías estratégicas y despliegue de agentes inteligentes (Manager, Closers, Content Hub). Elevamos la eficiencia de tu negocio con tecnología de vanguardia.',
  founderName: 'Nacho & David',
  founderTitle: 'Fundadores y Estrategas de IA',
  founderBio: 'En Agia 360, David (Londres) y Nacho (Madrid) combinan visión estratégica y ejecución técnica para ayudar a las empresas a navegar la era de la inteligencia artificial. Nuestra misión es automatizar lo operativo para que tú te centres en lo creativo.',
  yearsExperience: 1,
  yearFounded: 2025,

  contact: {
    phone: '+34600000000',
    phoneDisplay: '+34 600 000 000',
    email: 'contacto@agia360.ai',
    address: 'Madrid & London (Remote Hub)',
    city: 'Madrid',
    country: 'España',
    googleMapsEmbedUrl: '',
    whatsappNumber: '+34600000000',
    officeHours: 'Lunes a Viernes, 9:00 a.m. a 6:00 p.m.',
  },

  social: {
    facebook: 'https://facebook.com/agia360',
    instagram: 'https://instagram.com/agia360',
    linkedin: 'https://linkedin.com/company/agia360',
  },

  navigation: {
    items: [
      { label: 'Inicio', href: '/' },
      {
        label: 'Nuestros Agentes',
        href: '/servicios',
        children: [
          { label: 'Agente Manager', href: '/servicios#manager' },
          { label: 'Sales Closer', href: '/servicios#closer' },
          { label: 'Email Marketing', href: '/servicios#emkd' },
          { label: 'Content Hub', href: '/servicios#content' },
        ],
      },
      { label: 'Auditoría IA', href: '/equipo' },
      { label: 'Enfoque 360', href: '/#enfoque' },
      { label: 'Contacto', href: '/contacto' },
    ],
  },

  hero: {
    headline: 'Tus Agentes Expertos, Automatizados y Escalables',
    subheadline: 'Construimos el equipo de IA que tu negocio necesita para vender más y operar mejor. Auditoría gratuita de 360 grados.',
    ctaText: 'Empieza Ahora',
    ctaHref: '/contacto',
  },

  values: [
    {
      icon: 'experience',
      title: 'Innovación Constante',
      description: 'Nos mantenemos a la vanguardia de la IA para ofrecerte siempre las soluciones más eficientes y potentes.',
    },
    {
      icon: 'quality',
      title: 'Excelencia en Diseño',
      description: 'No solo creamos código, diseñamos experiencias que enamoran a tus usuarios y elevan tu marca.',
    },
    {
      icon: 'results',
      title: 'Orientación a Resultados',
      description: 'Nuestros agentes no son juguetes; son herramientas diseñadas para aumentar tu conversión y ROI.',
    },
  ],

  services: [
    {
      icon: 'custom',
      title: 'Agente Manager',
      slug: 'manager',
      shortDescription: 'El cerebro de tu operación. Orquestación inteligente de tareas y proyectos.',
      fullDescription: 'Nuestra IA orquestadora gestiona flujos de trabajo complejos, asigna tareas a otros agentes y supervisa el progreso en tiempo real, actuando como un Project Manager de alto nivel disponible 24/7.',
    },
    {
      icon: 'custom',
      title: 'Sales Closer',
      slug: 'closer',
      shortDescription: 'Convierte leads en clientes de forma automática y humanizada.',
      fullDescription: 'Agentes especializados en el cierre de ventas a través de chat o voz. Cualifican prospectos, resuelven dudas y cierran deals utilizando técnicas de persuasión avanzada y psicología de ventas.',
    },
    {
      icon: 'custom',
      title: 'Email Marketing',
      slug: 'emkd',
      shortDescription: 'Nurture semántico y automatización de newsletters de alta conversión.',
      fullDescription: 'Utilizamos el conocimiento de los mejores copywriters del mundo (Isra Bravo, Seth Godin, etc.) procesado a través de RAG para generar secuencias de correos que no parecen automáticos.',
    },
    {
      icon: 'custom',
      title: 'Content Hub',
      slug: 'content',
      shortDescription: 'Generación de contenido omnicanal manteniendo la voz de tu marca.',
      fullDescription: 'Transformamos una sola idea en piezas para LinkedIn, Twitter, blogs y más, asegurando coherencia estratégica y visual en todos tus canales digitales.',
    },
  ],

  tabs: [
    {
      title: 'Arquitectura 360',
      content: 'Analizamos tu negocio desde todos los ángulos para identificar cuellos de botella que la IA puede resolver. Desde la captación hasta el servicio post-venta.',
    },
    {
      title: 'Factory OS',
      content: 'Nuestro sistema operativo propietario permite desplegar agentes en cuestión de días, integrándose directamente con tu stack tecnológico actual.',
    },
    {
      title: 'Escalabilidad',
      content: 'Diseñamos soluciones que crecen contigo. Activa o desactiva módulos de agentes según las necesidades de tu pipeline y mercado.',
    },
  ],

  team: [
    {
      name: 'Nacho & David',
      title: 'Fundadores y Estrategas de IA',
      bio: 'En Agia 360, David (Londres) y Nacho (Madrid) combinan visión estratégica y ejecución técnica para transformar empresas tradicionales en potencias automatizadas.',
      specialties: ['Arquitectura de IA', 'Prompt Engineering', 'Estrategia Growth'],
    },
  ],

  testimonials: [
    {
      name: 'Elena R.',
      quote: 'El Agente Manager ha reducido mis horas de gestión operativa en un 70%. Agia 360 es el socio tecnológico que no sabía que necesitaba.',
      rating: 5,
      caseType: 'Eficiencia',
    },
    {
      name: 'Marc T.',
      quote: 'El Sales Closer automático ha mantenido nuestra tasa de cierre incluso fuera de horario laboral. Impresionante la calidad del lenguaje.',
      rating: 5,
      caseType: 'Ventas',
    },
  ],

  booking: {
    enabled: true,
    ctaText: 'Agendar Auditoría IA',
  },

  seo: {
    siteTitle: 'Agia 360 | Agencia de Inteligencia Artificial y Automatización',
    titleTemplate: '%s | Agia 360',
    defaultDescription: 'Agencia de IA especializada en auditorías estratégicas y agentes inteligentes (Manager, Closers, Content Hub). Innovación y eficiencia 360.',
    locale: 'es_ES',
  },

  legal: {
    privacyLastUpdated: '2026-04-20',
    termsLastUpdated: '2026-04-20',
  },
}
