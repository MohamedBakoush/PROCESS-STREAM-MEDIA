<script setup> 
const email = ref('')
const password = ref('')
const isSignUp = ref(false)
const loggedIn = ref(false)
const client = useSupabaseClient()

const supabaseUser = useSupabaseUser();
const router = useRouter();

const signUp = async () => {
  try {
    const { user, error } = await client.auth.signUp({
      email: email.value,
      password: password.value
    });

    if (user) {
      console.log('User signed up:', user);
    }

    if (error) {
      console.log(error);
      return;
    } 
  } catch (err) {
    console.error('Fetch error:', err);
  } finally {

    console.log(supabaseUser.value.id);
    const response = await fetch(`/api/addUser?supabase_user_id=${supabaseUser.value.id}`);

    // Check if the response is successful
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    loggedIn.value = true;
  }
};

const login = async () => {
  const { user, error } = await client.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })
  loggedIn.value = true;
  if (error) console.log(error)  
}

onMounted(() => {
  watchEffect(() => {
    if (supabaseUser.value) {
      router.push('/');
    }
  });
}) 
</script> 

<template>
  <div class="max-w-lg mx-auto mt-8"> 
    <form
      @submit.prevent="() => (isSignUp ? signUp() : login())"
      class="flex flex-col gap-2 mt-16"
    >
      <input
        type="email"
        placeholder="Email"
        v-model="email"
        class="p-2 rounded bg-charcoal-600"
      />
      <input
        type="password"
        placeholder="Password"
        v-model="password"
        class="p-2 rounded bg-charcoal-600"
      />
      <button
        type="submit"
        class="p-2 font-medium text-white bg-green-500 rounded hover:bg-green-400"
      >
        <span v-if="isSignUp"> Sign up </span>
        <span v-else> Log in </span>
      </button>
    </form>
    <button
      @click="isSignUp = !isSignUp"
      class="w-full mt-8 text-sm text-center underline text-slate-300"
    >
      <span v-if="isSignUp"> Have an account? Log in instead </span>
      <span v-else> Create a new account </span>
    </button>
  </div>
</template>